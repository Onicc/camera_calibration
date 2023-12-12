import cv2
from board import ChArUcoBoard

png_path = './calibration_board.png'

board, aruco_dict, board_name = ChArUcoBoard(width=12, height=8, square_length=0.024)
image_board = board.generateImage((3600, 2500), marginSize=100, borderBits=1)

cv2.putText(image_board, board_name, (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 8)
cv2.imwrite(png_path, image_board)
