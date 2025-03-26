import cv2
import os
import numpy as np
import time
import csv


class CameraController:
    def __init__(self):
        self.cap = None
    
    def open(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open camera.")
    
    def close(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
    
    def capture_frame(self):
        if not self.cap.isOpened():
            raise RuntimeError("Camera not open!")
        
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame.")
        return frame
    
    def process_image(self, i):
        frame = self.capture_frame()
        print(f"Processing image {i}")
        cv2.imshow('Frame', frame)
        cv2.waitKey(1)  # Needed to update OpenCV window

    def capture_frame(self):
        if not self.cap.isOpened():
            raise RuntimeError("Camera not open!")
        
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame.")
        return frame


    def process_image(self, i ):  # Added 'cap' parameter

        frame = self.capture_frame()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "data")
        img_dir = os.path.join(data_dir, "images")
        os.makedirs(img_dir, exist_ok=True)

        file_name = "RGB_values.csv"
        file_path = os.path.join(data_dir, file_name)

        frame_count = 0
        frame_buffer = 2
        lim = 360
        x, y, w, h = 306, 187, 118, 100  # Example: a 50x50 square at (100, 100)

        while True:

            # Extract ROI and calculate average color
            roi = frame[y:y+h, x:x+w]
            average_color = np.mean(roi, axis=(0, 1)).astype(int)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Sample_ID: {i}, Timestamp: {timestamp}, ROI Color (BGR): {average_color}")
            b, g, r = average_color

            # Draw rectangle around ROI
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow('Camera Stream', frame)
            
            frame_count += 1
            if frame_count > frame_buffer:
                if r + g + b > lim:
                    print("I think its blank")
                    return True
                else:
                    image_path = os.path.join(img_dir, f"img_{timestamp}.jpg")
                    cv2.imwrite(image_path, frame)
                    print(f"Saved: {image_path}")

                    with open(file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([i, timestamp, r, g, b])  # Separated RGB components

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.2)



if __name__ == "__main__":
    cam = open_camera()
    process_image(0, cam)
    process_image(1, cam)
    close_camera(cam)