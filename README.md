# Camera Calibration

[中文](./README_CN.md) | [English](./README.md)

This repository calibrates cameras using ChArUco markers, streamlining the camera calibration process.

## Installation

`camera_calibration` requires `opencv-contrib-python` and `opencv-python` version 4.7.0 or higher. Installing this package locally will automatically fetch other required dependencies.

```bash
git clone https://github.com/Onicc/camera_calibration.git
cd camera_calibration
pip install -r requirements.txt
```

## Usage

### Generate and Print Calibration Board
Run the following command to generate the calibration board. The path for the calibration board image is set to `./calibration_board.png`. You can also use the provided [calibration_board.png](./calibration_board.png). Print it out.

```bash
python3 generate_calibration_board.py
```

![calibration_board](./calibration_board.png)

### Camera Calibration

Measure the side length of the pure black squares on the calibration board in meters. Fill in the `square_length` on line 9 of [camera_calibration.py](./camera_calibration.py) with the measured value, for example, `0.024`.

```python
board, aruco_dict, board_name = ChArUcoBoard(width=12, height=8, square_length=0.024)
```

Capture images of the calibration board from different angles, collecting more than 20 images in PNG format, and store them in `./ChArUcoData`. Run the following command to calibrate. The calibration images will be displayed, press any key to switch to the next image.

```bash
python3 camera_calibration.py
```

After calibration, the command line will print camera parameters and distortion coefficients. The parameters will also be saved in `./params/camera_params.yaml`.

```
camera_matrix:
 [[3.03536832e+03 0.00000000e+00 2.01985797e+03]
 [0.00000000e+00 3.03628900e+03 1.48595051e+03]
 [0.00000000e+00 0.00000000e+00 1.00000000e+00]]
distortion_coefficients:
 [[ 1.98927651e-01 -8.93785973e-01 -9.71016301e-05 -6.80081320e-04
   1.60146884e+00]]
Calibration successful. Calibration file used: ./params/camera_params.yaml
```

### Estimate Camera Pose Using Calibration Parameters

Modify the image file path on line 59 of [detect_marker.py](./detect_marker.py). Run the following command, and it will automatically read the camera parameters from the YAML file, draw coordinate axes on the ChArUco markers, and print the rotation and translation vectors in the terminal.

```bash
python3 detect_marker.py
```

![iShot_2023-12-12_16.35.21](.assets/iShot_2023-12-12_16.35.21.jpg)

```
rvec:  [[ 1.85860902]
 [ 1.83634612]
 [-0.55535779]]
tvec:  [[-0.11929498]
 [-0.04856779]
 [ 0.42148201]]
```

## Reference

https://github.com/Jcparkyn/dpoint