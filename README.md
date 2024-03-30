# Lane Detection Project

## Overview

This project aims to detect lane lines in images or videos using computer vision techniques. The lane detection pipeline involves several steps, including image preprocessing, edge detection, Hough line detection, and lane line averaging. This README provides an overview of the process and includes visualizations of the intermediate results.

## Lane Detection Process

### 1. Original Image

![Original Image](https://github.com/ilayEldar24/Lane-Detection/blob/master/images/1.png)

The process begins with the original image captured by a camera mounted on a vehicle.

### 2. Grayscale Conversion

![Grayscale Image](https://github.com/ilayEldar24/Lane-Detection/blob/master/images/2.png)

The original image is converted to grayscale to simplify subsequent processing steps.

### 3. Gaussian Blurring

![Blurred Image](https://github.com/ilayEldar24/Lane-Detection/blob/master/images/3.png)

A Gaussian blur is applied to the grayscale image to reduce noise and smooth out details.

### 4. Edge Detection

![Edges Image](https://github.com/ilayEldar24/Lane-Detection/blob/master/images/4.png)

The Canny edge detection algorithm is used to identify edges in the blurred image.

### 5. Region of Interest Masking

![Masked Image](https://github.com/ilayEldar24/Lane-Detection/blob/master/images/6.png)

A region of interest (ROI) mask is applied to focus on the area where lane lines are expected.

### 6. Hough Line Detection

![Hough Lines Image](https://github.com/ilayEldar24/Lane-Detection/blob/master/images/7.png)

The Hough transform is applied to detect lines in the masked image.

### 7. Averaged Lane Lines

![Averaged Lines Image](https://github.com/ilayEldar24/Lane-Detection/blob/master/images/8.png)

Detected lines are averaged and extrapolated to generate stable lane lines.

### 8. Final Lane Detection

![Final Lanes Image](https://github.com/ilayEldar24/Lane-Detection/blob/master/images/9.png)

The averaged lane lines are overlaid onto the original image to visualize the detected lanes.

### 9. Video Processing

To process a video for lane detection, follow these steps:

1. Capture frames from the video using OpenCV.
2. Apply the lane detection pipeline to each frame individually.
3. Combine the processed frames into a new video using OpenCV.
4. Adjust parameters and settings as needed for optimal lane detection results.


## Usage

To use the lane detection pipeline on your own images or videos, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies (`numpy`, `opencv-python`, etc.).
3. Run the main script (`lane_detection.py`) with your input images or videos.
4. Adjust parameters as needed for optimal lane detection results.



## License

This project is licensed under the [MIT License](link_to_license).
