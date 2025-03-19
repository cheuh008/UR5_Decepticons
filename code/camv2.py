import cv2
import numpy as np
import time
import csv



def process_image(i):
    """Track the average color (in BGR) of the ROI. Since methylene blue is typically blue, checks for a significant drop in the Blue channel 
    (or for near-equal B, G, R values, signaling a fade to grey/white). When we detect that it's close to colorless 
    (e.g., all channels above a certain threshold and similar to each other), we stop capturing."""
    i += 1
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    x, y, w, h = 311, 108, 36, 46 # Example: a 50x50 square at (100, 100)
    csv_filename = f"RGB_values_Timedstamp.csv"
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sample ID', 'Timestamp', 'ROI Colour (BGR)'])
        print(f"Created new CSV file: {csv_filename}")

    # colourless_threshold = 170
    # tolerence = 20 #Allows slight varient in channels
    

    try:
        last_capture_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            roi = frame[y:y+h, x:x+w]
            average_color = np.mean(roi, axis=(0, 1)).astype(int)
            b, g, r = average_color

            # Get the current timestamp
            time.sleep(0.2)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Sample_ID: {i}, Timestamp: {timestamp}, ROI Color (BGR): {average_color}")
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw rectangle around ROI
            cv2.imshow('Camera Stream', frame)

            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i, timestamp, average_color])

            #Auto-stops condition when colour is "faded"
            if abs(r - g) < 20 or abs(g - b) < 20 or abs(r - b) < 20:
                break

            i += 1
                
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
        print("Colour Change Detected")
        return True


if __name__ == "__main__":
    process_image(0)
