# sanchitatripathy26IMSBIO025-
<h2 style="color: blue;">Task 1: Setup Repository &amp; Command Line Navigation</h2>
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
<h3 style="color: blue;">Task 2: Lane Detection &amp; Drivable Area Segmentation</h3>
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


<h4 style="color: blue;">Task 3: Obstacle &amp; Pothole Detection</h4>
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
### 📅 Date: September 13, 2026

#### 📌 Task 5 (Bonus): Introduction to ROS 2 Node Architecture
* *What I Did:*
  * Created Python scripts in Task_5/ implementing core ROS 2 communication interfaces (rclpy).
  * Implemented a *Publisher-Subscriber* model (topic_pub_sub.py) using std_msgs.msg.String for asynchronous status messaging over the ugv_status topic.
  * Implemented a *Service-Client* model (service_server_client.py) using example_interfaces.srv.AddTwoInts for synchronous request/response computation.

* *Problems Faced:*
  * Understanding the conceptual difference between continuous streaming (Topics) vs. request-response calls (Services).
  * Setting up node execution loops within Python client scripts.

* *What I Learnt:*
  * *Topics:* Best for continuous sensor telemetry and real-time streaming data.
  * *Services:* Best for discrete actions, state triggers, and target computations that require explicit confirmation.
### 🗓️ Date: September 13, 2026

📌 *Task 4: Autonomous Path Planning & Navigation System*

* What I Did:

    * Created a Python script (path_planning.py) inside Task_4/ to process track imagery, detect hazards, and plan safe navigation paths using OpenCV.
    * Implemented road isolation using Contrast Limited Adaptive Histogram Equalization (CLAHE) and adaptive Otsu thresholding with morphological operations.
    * Developed detection logic for dark ringed potholes (bounding red boxes) and obstacle markers (bounding yellow boxes) based on color segmentation in HSV space.
    * Applied Distance Transform mapping (cv2.distanceTransform) on safe drivable road regions to dynamically calculate and render optimal high-clearance green navigation paths.

* Problems Faced:

    * Fine-tuning morphological filter parameters to isolate track contours without merging nearby obstacles into road boundaries.
    * Filtering out false positives such as painted white text and start arrow indicators during hazard mask generation.

* What I Learnt:

    * Distance Transform Navigation: Understood how Euclidean distance field maps extract middle-ridge skeletons for safest trajectory generation.
    * Safety Buffering: Practiced structural dilation to generate dynamic clearance zones around active track obstacles.