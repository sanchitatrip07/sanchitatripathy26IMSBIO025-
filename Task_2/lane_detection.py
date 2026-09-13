import cv2
import numpy as np
import os

def detect_lane(image_path, output_path):
    # 1. Load the original image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image at {image_path}")
        return

    # 2. Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. Apply Gaussian Blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 4. Canny Edge Detection
    edges = cv2.Canny(blur, 50, 150)

    # 5. Define Region of Interest (ROI) - focus on road area
    height, width = edges.shape
    mask = np.zeros_like(edges)
    polygon = np.array([[
        (0, height),
        (width, height),
        (int(width * 0.8), int(height * 0.55)),
        (int(width * 0.2), int(height * 0.55))
    ]], np.int32)
    cv2.fillPoly(mask, polygon, 255)
    masked_edges = cv2.bitwise_and(edges, mask)

    # 6. Hough Transform to detect line segments
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, threshold=40, minLineLength=20, maxLineGap=100)

    # 7. Classify lines into left and right lane boundaries
    left_fit = []
    right_fit = []

    if lines is not None:
        for line in lines:
            line_data = line.reshape(-1)
            if len(line_data) < 4:
                continue
            x1, y1, x2, y2 = line_data[:4]
            if x2 == x1:
                continue  # Avoid division by zero
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1

            # Filter out near-horizontal noise
            if abs(slope) < 0.3:
                continue

            if slope < 0:  # Negative slope = Left lane line
                left_fit.append((slope, intercept))
            else:          # Positive slope = Right lane line
                right_fit.append((slope, intercept))

    # Calculate average boundary line endpoints
    y1 = height
    y2 = int(height * 0.6)

    overlay = image.copy()
    
    def make_points(line_fit):
        if len(line_fit) == 0:
            return None
        slope, intercept = np.mean(line_fit, axis=0)
        if abs(slope) < 1e-5:
            return None
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        return [(x1, y1), (x2, y2)]

    left_line = make_points(left_fit)
    right_line = make_points(right_fit)

    # 8. Draw drivable area (green) and detected boundary lines
    if left_line and right_line:
        pts = np.array([
            left_line[0], left_line[1],
            right_line[1], right_line[0]
        ], np.int32)
        cv2.fillPoly(overlay, [pts], (0, 255, 0))  # Green fill
        output_img = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)
        
        cv2.line(output_img, left_line[0], left_line[1], (0, 0, 255), 5)   # Red left boundary
        cv2.line(output_img, right_line[0], right_line[1], (255, 0, 0), 5)  # Blue right boundary
    else:
        output_img = image

    # Save output image to output folder
    cv2.imwrite(output_path, output_img)
    print(f"Processed and saved: {output_path}")

# Process all images inside Task_2/input
input_dir = "Task_2/input"
output_dir = "Task_2/output"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for file_name in os.listdir(input_dir):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        in_path = os.path.join(input_dir, file_name)
        out_path = os.path.join(output_dir, file_name)
        detect_lane(in_path, out_path)