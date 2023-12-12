import cv2
from cv2 import aruco
import numpy as np
from typing import Tuple

from board import ChArUcoBoard

def read_camera_parameters(filename: str) -> Tuple[np.ndarray, np.ndarray]:
    fs = cv2.FileStorage(filename, cv2.FILE_STORAGE_READ)
    if not fs.isOpened():
        raise Exception("Couldn't open file")
    camera_matrix = fs.getNode("camera_matrix").mat()
    dist_coeffs = fs.getNode("distortion_coefficients").mat()
    fs.release()
    return (camera_matrix, dist_coeffs)

camera_matrix, dist_coeffs = read_camera_parameters("params/camera_params.yaml")
board, aruco_dict, board_name = ChArUcoBoard(width=12, height=8, square_length=0.024)
parameters =  aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

def estimate_camera_pose_charuco(frame, camera_matrix, dist_coeffs):
    corners, ids, rejected = detector.detectMarkers(frame)
    if len(corners) == 0:
        raise Exception("No markers detected")
    display_frame = aruco.drawDetectedMarkers(image=frame, corners=corners)
    num_corners, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
        markerCorners=corners, markerIds=ids, image=frame, board=board
    )
    if num_corners < 5:
        raise Exception("Not enough corners detected")
    display_frame = aruco.drawDetectedCornersCharuco(
        image=display_frame, charucoCorners=charuco_corners, charucoIds=charuco_ids
    )
    success, rvec, tvec = aruco.estimatePoseCharucoBoard(
        charuco_corners,
        charuco_ids,
        board,
        camera_matrix,
        dist_coeffs,
        None,
        None,
        False,
    )
    if not success:
        raise Exception("Failed to estimate camera pose")
    # The rvec from charuco is z-down for some reason.
    # This is a hack to convert back to z-up.
    rvec, *_ = cv2.composeRT(np.array([0, 0, -np.pi / 2]), tvec * 0, rvec, tvec)
    rvec, *_ = cv2.composeRT(np.array([0, np.pi, 0]), tvec * 0, rvec, tvec)
    display_frame = cv2.drawFrameAxes(
        display_frame, camera_matrix, dist_coeffs, rvec, tvec, 0.2
    )
    cv2.imshow("Charuco", display_frame)
    return (rvec, tvec)

image = cv2.imread("your_image.png")
rvec, tvec = estimate_camera_pose_charuco(image, camera_matrix, dist_coeffs)
print("rvec: ", rvec)
print("tvec: ", tvec)
cv2.waitKey(0)
