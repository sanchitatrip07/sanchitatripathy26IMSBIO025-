# sanchitatripathy26IMSBIO025-
## Task 1: Setup Repository & Command Line Navigation
​What I Did:
​Created the official GitHub repository named sanchitatripathy26IMSBIO025.
​Configured local Git credentials, established tracking branches, and initialized directory structures for tasks (Task_1, Task_2, Task_3, Task_4).
​Practiced core Git CLI workflows: git clone, git add, git commit, git push, git status, and git checkout for revision recovery.
​Created, modified, and managed files directly using PowerShell / terminal commands (mkdir, touch, cp, mv).
​Problems Faced:
​Initial authentication errors while pushing code to remote GitHub repository via VS Code terminal.
​Path navigation mismatches when executing scripts across nested subdirectories.
​What I Learnt:
​Learned how to set up Personal Access Tokens (PAT) and SSH keys for secure GitHub CLI operations.
​Mastered relative vs. absolute file paths in terminal navigation and script execution.
​📅 Date: September 12, 2026
### Task 2: Lane Detection & Drivable Area Segmentation
​What I Did:
​Developed Task_2/main_task2.py using Python and OpenCV to isolate asphalt road boundaries and highlight the drivable region between them.
​Implemented HSV color segmentation (cv2.cvtColor, cv2.inRange) to filter out background elements and isolate the light-grey road surface.
​Extracted left and right lane boundary markers (blue and orange blocks) framing the circuit.
​Applied semi-transparent green overlays using cv2.addWeighted to visually highlight the drivable lane region.
​Problems Faced:
​High lighting variance and shadows across images caused standard grayscale thresholding to mistakenly classify the dark background outside the map as road surface.
​Morphological noise created broken lane contours along tight curves.
​What I Learnt:
​Discovered that HSV (Hue, Saturation, Value) color space is far superior to standard RGB/BGR for separating road surfaces based on low saturation values.
​Applied morphological operators (cv2.MORPH_CLOSE, cv2.MORPH_OPEN) with elliptical kernels to smooth segment boundaries and bridge contour gaps.
​📅 Date: September 13, 2026
​#### Task 3: Obstacle & Pothole Detection
​What I Did:
​Developed Task_3/main_task3.py to identify dark circular potholes and red obstacle blocks located on the drivable track.
​Implemented dual-range HSV thresholding to capture red obstacles across hue boundaries ([0, 10] and [160, 180]).
​Segmented dark potholes by combining low-intensity thresholding (V < 65) with a bitwise mask of the drivable road surface to eliminate background false positives.
​Generated bounding boxes (cv2.boundingRect) around all detected hazards, annotated pixel coordinates (x, y, w, h), and overlayed a dynamic total count of detected obstacles on every output image.
​Problems Faced:
​Dark background areas outside the track map were initially being misclassified as road potholes.
​Tiny pixel noise and color artifacts produced false-positive bounding boxes around clean road segments.
​What I Learnt:
​Solved false-positive detections by masking dark spot queries strictly inside the verified road region using cv2.bitwise_and.
​Filtered detected contours based on minimum and maximum contour area thresholds (cv2.contourArea) to filter out noise while keeping actual hazards