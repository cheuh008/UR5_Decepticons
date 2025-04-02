import cv2
import os
import numpy as np
import time
import csv
import threading

class CameraController:
    def __init__(self):
        self.running = False
        self.cap = None
        self.lock = threading.Lock()
        self.current_frame = None
        self.x, self.y, self.w, self.h = 306, 187, 118, 100  # ROI coordinates
        self.frame_buffer = 2
        self.lim = 360

    def start_capture(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")
        
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.current_frame = frame.copy()
                
                # Display feed
                cv2.rectangle(frame, (self.x, self.y), (self.x+self.w, self.y+self.h), (0, 255, 0), 2)
                cv2.imshow('Camera Feed', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            time.sleep(0.02)  # Reduce CPU usage
        
        self.cap.release()
        cv2.destroyAllWindows()

    def process_image(self, i):
        # Setup directories
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "data")
        img_dir = os.path.join(data_dir, "images")
        os.makedirs(img_dir, exist_ok=True)
        file_path = os.path.join(data_dir, "RGB_values.csv")

        frame_count = 0
        blank_detected = False

        while frame_count <= self.frame_buffer and not blank_detected:
            with self.lock:
                if self.current_frame is None:
                    time.sleep(0.1)
                    continue
                
                frame = self.current_frame.copy()
            
            # Process frame
            roi = frame[self.y:self.y+self.h, self.x:self.x+self.w]
            average_color = np.mean(roi, axis=(0, 1)).astype(int)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            b, g, r = average_color
            print(f"Sample_ID: {i}, Timestamp: {timestamp}, ROI Color (RGB): {average_color}")

            if frame_count > 0:  # Skip first frame (often has artifacts)
                if r + g + b > self.lim:
                    print("Blank detected")
                    blank_detected = True
                else:
                    image_path = os.path.join(img_dir, f"img_{i}_{timestamp}.jpg")
                    cv2.imwrite(image_path, frame)
                    with open(file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([i, timestamp, r, g, b])
            
            frame_count += 1
            time.sleep(0.1)
        
        return blank_detected

    def stop(self):
        self.running = False

    

if __name__ == '__main__':

    camera = CameraController()
    cam_thread = threading.Thread(target=camera.start_capture)
    cam_thread.start()

    is_blank = False
    while not is_blank:
        is_blank = camera.process_image(0)
        time.sleep(0.2)

    camera.stop()
    cam_thread.join()