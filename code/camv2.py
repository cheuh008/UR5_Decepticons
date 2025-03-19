import cv2
import numpy as np
import time
import csv

"""Track the average color (in BGR) of the ROI. Since methylene blue is typically blue, checks for a significant drop in the Blue channel 
(or for near-equal B, G, R values, signaling a fade to grey/white). When we detect that it's close to colorless 
(e.g., all channels above a certain threshold and similar to each other), we stop capturing."""

def process_image(i):
    i += 1
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is the default camera

    # Define the region of interest (ROI) coordinates
    x, y, w, h = 100, 100, 50, 50  # Example: a 50x50 square at (100, 100)

    # Create a CSV
    csv_filename = f"RGB_values_Timedstamp.csv"

    # Open a new CSV file to write the data
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write headers
        writer.writerow(['Sample ID', 'Timestamp', 'ROI Colour (BGR)'])
        print(f"Created new CSV file: {csv_filename}")

    colourless_threshold = 170
    tolerence = 20 #Allows slight varient in channels
    

    try:
        last_capture_time = time.time()

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break

            # Extract the ROI
            roi = frame[y:y+h, x:x+w]

            # Calculate the average color of the ROI
            average_color = np.mean(roi, axis=(0, 1)).astype(int)
            b, g, r = average_color

            # Get the current timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # Print the color data to the console
            print(f"Sample_ID: {i}, Timestamp: {timestamp}, ROI Color (BGR): {average_color}")

            # Display the frame with the ROI highlighted
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw rectangle around ROI
            cv2.imshow('Camera Stream', frame)

            # Save the data to the new CSV
            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i, timestamp, average_color])

            #Auto-stops condition when colour is "faded"
            if (
                b > colourless_threshold and
                g > colourless_threshold and
                r > colourless_threshold and
                abs(b - g) < tolerence and
                abs(g - r) < tolerence and
                abs(b - r) < tolerence
            ):
                break

            i += 1
                
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    process_image(0)