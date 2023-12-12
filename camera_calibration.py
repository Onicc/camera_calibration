
import cv2
from cv2 import aruco
import glob
from pathlib import Path

from board import ChArUcoBoard

board, aruco_dict, board_name = ChArUcoBoard(width=12, height=8, square_length=0.024)

# Create the arrays and variables we'll use to store info like corners and IDs from images processed
corners_all = []    # Corners discovered in all images processed
ids_all = []        # Aruco ids corresponding to corners discovered
image_size = None   # Determined at runtime

images = glob.glob('./ChArUcoData/*.png')

for iname in images:
    # Open the image
    img = cv2.imread(iname)
    # Grayscale the image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find aruco markers in the query image
    corners, ids, _ = aruco.detectMarkers(
            image=gray,
            dictionary=aruco_dict)

    # Outline the aruco markers found in our query image
    img = aruco.drawDetectedMarkers(
            image=img, 
            corners=corners)

    # Get charuco corners and ids from detected aruco markers
    response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
            markerCorners=corners,
            markerIds=ids,
            image=gray,
            board=board)

    # If a Charuco board was found, let's collect image/corner points
    # Requiring at least 20 squares
    if response > 20:
        # Add these corners and ids to our calibration arrays
        corners_all.append(charuco_corners)
        ids_all.append(charuco_ids)
        
        # Draw the Charuco board we've detected to show our calibrator the board was properly detected
        img = aruco.drawDetectedCornersCharuco(
                image=img,
                charucoCorners=charuco_corners,
                charucoIds=charuco_ids)
       
        # If our image size is unknown, set it now
        if not image_size:
            image_size = gray.shape[::-1]
    
        # Reproportion the image, maxing width or height at 1000
        proportion = max(img.shape) / 1000.0
        img = cv2.resize(img, (int(img.shape[1]/proportion), int(img.shape[0]/proportion)))
        # Pause to display each image, waiting for key press
        cv2.imshow('Charuco board', img)
        cv2.waitKey(0)
    else:
        print("Not able to detect a charuco board in image: {}".format(iname))

# Destroy any open CV windows
cv2.destroyAllWindows()

# Make sure at least one image was found
if len(images) < 1:
    # Calibration failed because there were no images, warn the user
    print("Calibration was unsuccessful. No images of charucoboards were found. Add images of charucoboards and use or alter the naming conventions used in this file.")
    # Exit for failure
    exit()

# Make sure we were able to calibrate on at least one charucoboard by checking
# if we ever determined the image size
if not image_size:
    # Calibration failed because we didn't see any charucoboards of the PatternSize used
    print("Calibration was unsuccessful. We couldn't detect charucoboards in any of the images supplied. Try changing the patternSize passed into Charucoboard_create(), or try different pictures of charucoboards.")
    # Exit for failure
    exit()

# Now that we've seen all of our images, perform the camera calibration
# based on the set of points we've discovered
calibration, camera_matrix, dist_coeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
        charucoCorners=corners_all,
        charucoIds=ids_all,
        board=board,
        imageSize=image_size,
        cameraMatrix=None,
        distCoeffs=None)
    
# Print matrix and distortion coefficient to the console
print("camera_matrix:\n", camera_matrix)
print("distortion_coefficients:\n", dist_coeffs)

output_path = "./params/camera_params.yaml"
Path(output_path).parent.mkdir(parents=True, exist_ok=True)
fs = cv2.FileStorage(output_path, cv2.FILE_STORAGE_WRITE)
if not fs.isOpened():
    raise Exception("Couldn't open file")
fs.write("camera_matrix", camera_matrix)
fs.write("distortion_coefficients", dist_coeffs)
fs.release()

print(f"Calibration successful. Calibration file used: {output_path}")
