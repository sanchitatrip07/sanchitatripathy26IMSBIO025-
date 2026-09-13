import cv2
import numpy as np
import os

def detect_obstacles_and_potholes(image_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image at {image_path}")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Thresholding to segment white circular blobs/potholes & bright obstacles
    _, thresholded = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)

    # Find contours (outlines of detected shapes)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    pothole_count = 0
    obstacle_count = 0

    output_img = image.copy()

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 30:  # Ignore tiny noise spots
            continue

        # Get bounding box coordinates: (x, y, width, height)
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Calculate aspect ratio and circularity to differentiate shapes
        aspect_ratio = float(w) / h
        perimeter = cv2.arcLength(cnt, True)
        circularity = 4 * np.pi * (area / (perimeter * perimeter)) if perimeter > 0 else 0

        # Classify as Pothole (circular) or general Obstacle
        if circularity > 0.6 and 0.7 <= aspect_ratio <= 1.3:
            label = f"Pothole ({x},{y})"
            color = (0, 0, 255)  # Red for Potholes
            pothole_count += 1
        else:
            label = f"Obstacle ({x},{y})"
            color = (0, 255, 255)  # Yellow for Obstacles
            obstacle_count += 1

        # Draw rectangular bounding box
        cv2.rectangle(output_img, (x, y), (x + w, y + h), color, 2)

        # Print pixel coordinates text above bounding box
        cv2.putText(output_img, label, (x, max(y - 5, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    # Display total counts on top left of image
    summary_text = f"Potholes: {pothole_count} | Obstacles: {obstacle_count}"
    cv2.putText(output_img, summary_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Save output image
    cv2.imwrite(output_path, output_img)
    print(f"File: {os.path.basename(image_path)} -> Found {pothole_count} Potholes & {obstacle_count} Obstacles. Saved to {output_path}")

# Run detection for all images in Task_3/input
input_dir = "Task_3/input"
output_dir = "Task_3/output"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for file_name in os.listdir(input_dir):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        in_path = os.path.join(input_dir, file_name)
        out_path = os.path.join(output_dir, file_name)
        detect_obstacles_and_potholes(in_path, out_path)