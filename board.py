import cv2

def ChArUcoBoard(width, height , square_length):
    marker_length=square_length*6/8

    dictionary = cv2.aruco.DICT_4X4_50
    dict_name = "DICT_4X4_50"
    board_name = ("ChArUco_OpenCV-" + cv2.__version__ + "_" + str(width) + "x" + str(height) + "_" + dict_name)
    
    aruco_dict = cv2.aruco.getPredefinedDictionary(dictionary)
    
    board = cv2.aruco.CharucoBoard(
        size=[width, height],
        squareLength=square_length,
        markerLength=marker_length,
        dictionary=aruco_dict,
    )

    return board, aruco_dict, board_name
