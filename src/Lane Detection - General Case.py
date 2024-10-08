# -*- coding: utf-8 -*-
"""Lane_Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11gxr9F-k_VnYWBdA-xbSgvjbGm1R-7VV
"""

from google.colab import drive
from google.colab import files
from google.colab.patches import cv2_imshow
import os
import numpy as np


# Mount Google Drive
drive.mount('/content/drive')

# Define the filename
video_filename = 'Dashcam Video.mp4'


video_path = '/content/drive/My Drive/' + video_filename

if os.path.exists(video_path):
    print(f"{video_filename} exists in your Google Drive.")
else:
    print(f"{video_filename} not found in your Google Drive. Please make sure the file is uploaded to your Drive.")

# If the file exists in Google Drive, Copying into colab enviorment
if os.path.exists(video_path):
    # Copy the video file to the Colab working directory
    !cp "{video_path}" "./{video_filename}"
    print(f"{video_filename} has been copied to the Colab environment.")
else:
    print(f"File {video_filename} not found in your Google Drive. Please upload it to your Drive or provide the correct file path.")

import cv2

# Define the video filename
video_filename = 'Dashcam Video.mp4'

# Open the video file
cap = cv2.VideoCapture(video_filename)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
else:
    print("Video opened successfully.")

# Open the video file again
cap = cv2.VideoCapture('Dashcam Video.mp4')

# Determine the video's frame rate
fps = cap.get(cv2.CAP_PROP_FPS)

# Calculate the number of frames to capture for 5 seconds
duration_seconds = 25
frames_count = int(duration_seconds * fps)

# Read and store frames from the video
frames = []
for i in range(frames_count):
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

cap.release()  # Release the video capture object

# Save the 5-second clip as a new video
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('5_sec_clip.mp4', fourcc, fps, (frames[0].shape[1], frames[0].shape[0]))
for frame in frames:
    out.write(frame)
out.release()

def make_points(image, average):
 slope, y_int = average
 y1 = image.shape[0]
 y2 = int(y1 * (3/5))
 x1 = int((y1 - y_int) // slope)
 x2 = int((y2 - y_int) // slope)
 return np.array([x1, y1, x2, y2])

def average(image, lines):
    left = []
    right = []
    if lines is None or len(lines) == 0:  # Check if lines is None or empty
        return (None)  # Return default value if lines is None or empty
    for line in lines:
        print(line)
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        y_int = parameters[1]
        if slope < 0:
            left.append((slope, y_int))
        else:
            right.append((slope, y_int))
    if right:
        right_avg = np.average(right, axis=0)
    else:
        right_avg = np.array([0, 0])  # Provide default values if no right lines
    if left:
        left_avg = np.average(left, axis=0)
    else:
        left_avg = np.array([0, 0])   # Provide default values if no left lines

    left_line = make_points(image, left_avg)
    right_line = make_points(image, right_avg)
    return np.array([left_line, right_line])


def roi_mask(image):
    height, width = image.shape[:2]

    # Calculate the height of the polygon
    mid_x, mid_y = width // 2, height // 2

# Region of interest (ROI) vertices for a pentagon
    roi_vertices = np.array([
        [width, int(height * 0.85)],    # Bottom right (just above the cut)
        [mid_x*0.95, mid_y*1.08],                 # Middle of the image
        [0, int(height * 0.85)]         # Bottom left (just above the cut)
    ], dtype=np.int32)

    # Create a mask for the region of interest (ROI)
    roi_mask = np.zeros_like(image)
    # Fill the pentagon on the mask
    roi_mask = cv2.fillPoly(roi_mask, [roi_vertices], 255)
    return roi_mask

def display_lines(image, lines):
 lines_image = np.zeros_like(image)
 if lines is not None:
   for line in lines:
     x1, y1, x2, y2 = line
     cv2.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
 return lines_image

copy = np.copy(frames[0])
cv2_imshow(copy)
gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
cv2_imshow(gray)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
cv2_imshow(blurred)
edges = cv2.Canny(blurred, 30, 120)
cv2_imshow(edges)
mask = roi_mask(edges)
cv2_imshow(mask)
masked_image = cv2.bitwise_and(edges, mask)
cv2_imshow(masked_image)
lines = cv2.HoughLinesP(masked_image, 1, np.pi/180, threshold=70, minLineLength=30, maxLineGap=50)
averaged_lines = average(masked_image, lines)
black_lines = display_lines(copy, averaged_lines)
lanes = cv2.addWeighted(copy, 0.8, black_lines, 1, 1)
cv2_imshow(lanes)

# Initialize video writer
output_filename = 'annotated_20_sec_clip.mp4'
out = cv2.VideoWriter(output_filename, fourcc, fps, (frames[0].shape[1], frames[0].shape[0]))
previous_lanes = None

for frame in frames:
  copy = np.copy(frame)
  gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
  blurred = cv2.GaussianBlur(gray, (5,5), 0)
  edges = cv2.Canny(blurred, 30, 120)
  mask = roi_mask(edges)
  masked_image = cv2.bitwise_and(edges, mask)
  lines = cv2.HoughLinesP(masked_image, 1, np.pi/180, threshold=70, minLineLength=30, maxLineGap=50)
  averaged_lines = average(masked_image, lines)
  if lines is None or len(lines) == 0:
    if previous_lanes != None:
      averaged_lines = previous_lanes
    else:
      out.write(copy)
      continue
  black_lines = display_lines(copy, averaged_lines)
  lanes = cv2.addWeighted(copy, 0.8, black_lines, 1, 1)
  out.write(lanes)


# Release everything when job is finished
out.release()

print("Video processing is complete. The video has been saved to the Colab environment.")

# Use the 'files.download' function to prompt the browser to download the file to your local machine
files.download('annotated_20_sec_clip.mp4')

