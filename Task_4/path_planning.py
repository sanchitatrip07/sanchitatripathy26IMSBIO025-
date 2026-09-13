import cv2
import numpy as np
import os
import glob

# Setup paths for Task_4 directory structure

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

# Ensure directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def process_perfect_navigation(img_path):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Could not read image at: {img_path}")
        return

    h, w, _ = img.shape
    file_name = os.path.basename(img_path)
    output_img = img.copy()

    # --- 1. PRE-PROCESSING & ROAD ISOLATION ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Local Contrast Enhancement for low-gray separation
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Adaptive thresholding to segment light gray road track
    blur = cv2.GaussianBlur(enhanced, (9, 9), 0)
    _, track_thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Clean morphological noise
    kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    track_clean = cv2.morphologyEx(track_thresh, cv2.MORPH_CLOSE, kernel_large)
    track_clean = cv2.morphologyEx(track_clean, cv2.MORPH_OPEN, kernel_large)

    # Find the main continuous track contour
    cnts, _ = cv2.findContours(track_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    track_mask = np.zeros((h, w), dtype=np.uint8)
    if cnts:
        road_cnt = max(cnts, key=cv2.contourArea)
        cv2.drawContours(track_mask, [road_cnt], -1, 255, -1)

    # --- 2. ACCURATE POTHOLE DETECTION (Dark Ellipses/Rings) ---
    dark_core = cv2.inRange(gray, 0, 50)
    dark_core_on_track = cv2.bitwise_and(dark_core, track_mask)

    p_cnts, _ = cv2.findContours(dark_core_on_track, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pothole_mask = np.zeros((h, w), dtype=np.uint8)
    pothole_count = 0

    for c in p_cnts:
        area = cv2.contourArea(c)
        if 50 < area < 1800:
            x, y, bw, bh = cv2.boundingRect(c)
            aspect_ratio = float(bw) / bh
            if 0.5 <= aspect_ratio <= 1.8:
                pothole_count += 1
                cv2.rectangle(output_img, (x - 3, y - 3), (x + bw + 3, y + bh + 3), (0, 0, 255), 2)  # Red Box
                cv2.drawContours(pothole_mask, [c], -1, 255, -1)

    # --- 3. OBSTACLE DETECTION (Cones / Squares / Colored Dots) ---
    s_channel = hsv[:, :, 1]
    color_objects = cv2.inRange(s_channel, 30, 255)

    tan_squares = cv2.inRange(gray, 140, 190)

    combined_obs = cv2.bitwise_or(color_objects, tan_squares)

    # Filter white arrow & text
    white_text = cv2.inRange(gray, 220, 255)
    combined_obs = cv2.bitwise_and(combined_obs, cv2.bitwise_not(white_text))
    obs_on_track = cv2.bitwise_and(combined_obs, track_mask)

    o_cnts, _ = cv2.findContours(obs_on_track, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    obstacle_mask = np.zeros((h, w), dtype=np.uint8)
    obstacle_count = 0

    for c in o_cnts:
        area = cv2.contourArea(c)
        if 30 < area < 1500:
            obstacle_count += 1
            x, y, bw, bh = cv2.boundingRect(c)
            cv2.rectangle(output_img, (x - 2, y - 2), (x + bw + 2, y + bh + 2), (0, 255, 255), 2)  # Yellow Box
            cv2.drawContours(obstacle_mask, [c], -1, 255, -1)

    # --- 4. START POINT DETECTION ---
    start_pos = None
    w_cnts, _ = cv2.findContours(white_text, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if w_cnts:
        arrow_c = max(w_cnts, key=cv2.contourArea)
        M = cv2.moments(arrow_c)
        if M["m00"] != 0:
            start_pos = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # --- 5. DRIVABLE PATH PLANNING ---
    all_hazards = cv2.bitwise_or(pothole_mask, obstacle_mask)
    safety_buffer = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
    expanded_hazards = cv2.dilate(all_hazards, safety_buffer)

    safe_road = cv2.subtract(track_mask, expanded_hazards)

    dist_map = cv2.distanceTransform(safe_road, cv2.DIST_L2, 5)

    if dist_map.max() > 0:
        _, skeleton = cv2.threshold(dist_map, 0.22 * dist_map.max(), 255, cv2.THRESH_BINARY)
        skeleton = np.uint8(skeleton)

        smooth_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        skeleton = cv2.morphologyEx(skeleton, cv2.MORPH_CLOSE, smooth_kernel)

        path_contours, _ = cv2.findContours(skeleton, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if path_contours:
            cv2.drawContours(output_img, path_contours, -1, (0, 255, 0), 3)

    # --- 6. DRAW START MARKER & STATS ---
    if start_pos:
        cv2.circle(output_img, start_pos, 7, (255, 0, 0), -1)
        cv2.putText(output_img, "START", (start_pos[0] + 10, start_pos[1] + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 2)

    cv2.putText(output_img, f"Detected Potholes: {pothole_count} | Obstacles: {obstacle_count}",
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    # Save & Display locally
    output_path = os.path.join(OUTPUT_DIR, file_name)
    cv2.imwrite(output_path, output_img)

    print(f"Successfully Processed & Saved: {output_path}")

    # Display window (press any key to move to the next image)
    cv2.imshow('Processed Path Navigation', output_img)
    cv2.waitKey(0)


# Run All Supported Images in input directory
supported_extensions = ('*.png', '*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.bmp')
image_list = []

for ext in supported_extensions:
    # Uses os.path.join so pathing is correct regardless of OS
    image_list.extend(glob.glob(os.path.join(INPUT_DIR, ext)))

if not image_list:
    print(f"No images found in '{INPUT_DIR}'. Please place your images there.")
else:
    for img_path in image_list:
        process_perfect_navigation(img_path)

    cv2.destroyAllWindows()