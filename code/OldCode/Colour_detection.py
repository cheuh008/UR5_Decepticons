import cv2
import numpy as np
import time
import csv

# Define color thresholds for red and blue
RED_THRESHOLD = (175, 158, 157)  # (R, G, B)
BLUE_THRESHOLD = (164, 180, 187)  # (R, G, B)

def is_coloured(average_color):
    """
    Determine if the solution is colored (red or blue) using RGB sum thresholds.
    :param average_color: The average BGR color of the ROI.
    :return: True if red or blue is detected, False otherwise.
    """
    blue, green, red = average_color  # OpenCV uses BGR format

    # Compute the sum of RGB values
    rgb_sum = red + green + blue
    red_sum = sum(RED_THRESHOLD)
    blue_sum = sum(BLUE_THRESHOLD)

    # Check if the sum of the ROI's color meets or exceeds the threshold
    return rgb_sum >= red_sum or rgb_sum >= blue_sum

def process_image(i):
    i += 1
    cap = cv2.VideoCapture(0)  # 0 is the default camera

    # Define the region of interest (ROI) coordinates
    x, y, w, h = 100, 100, 50, 50  # Example: a 50x50 square at (100, 100)

    # Create a CSV
    csv_filename = f"RGB_values_Timestamp.csv"

    # Open a new CSV file to write the data
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sample ID', 'Timestamp', 'ROI Colour (BGR)', 'RGB Sum', 'Colored?'])
        print(f"Created new CSV file: {csv_filename}")

    try:
        # Capture the first frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            return

        # Extract the ROI and compute the average color
        roi = frame[y:y+h, x:x+w]
        average_color = np.mean(roi, axis=(0, 1)).astype(int)

        # Compute RGB sum
        rgb_sum = sum(average_color)

        # Get timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Determine if the sample is colored
        colored = is_coloured(average_color)
        print(f"Sample_ID: {i}, Timestamp: {timestamp}, ROI Color (BGR): {average_color}, RGB Sum: {rgb_sum}, Colored: {colored}")

        # Save to CSV
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i, timestamp, list(average_color), rgb_sum, "Yes" if colored else "No"])

        # Display frame with ROI
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow('Camera Stream', frame)
        cv2.waitKey(1000)  # Display for 1 second

        # If colorless, stop capturing
        if not colored:
            print("Solution is colorless. Stopping further captures.")
            return

        # If colored, capture more images
        for _ in range(2):  # Capture 2 more images
            time.sleep(1)
            ret, frame = cap.read()
            if not ret:
                break

            roi = frame[y:y+h, x:x+w]
            average_color = np.mean(roi, axis=(0, 1)).astype(int)
            rgb_sum = sum(average_color)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            print(f"Sample_ID: {i}, Timestamp: {timestamp}, ROI Color (BGR): {average_color}, RGB Sum: {rgb_sum}")

            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i, timestamp, list(average_color), rgb_sum, "Yes"])

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow('Camera Stream', frame)
            cv2.waitKey(1000)

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    process_image(0)
