import os
import cv2
import csv
import time
import threading
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from collections import deque
import numpy as np

class CameraController:
    def __init__(self):
        self.running = False
        self.cap = None
        self.lock = threading.Lock()
        self.current_frame = None
        self.x, self.y, self.w, self.h = 306, 187, 118, 100  # ROI coordinates
        self.frame_buffer = 2
        self.lim = 360
        
        # For live plotting
        self.max_data_points = 100  # How many points to show in the plot
        self.time_data = deque(maxlen=self.max_data_points)
        self.r_data = deque(maxlen=self.max_data_points)
        self.g_data = deque(maxlen=self.max_data_points)
        self.b_data = deque(maxlen=self.max_data_points)
        
        # Initialize plot figure
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.set_xlabel('Time (s)', fontsize=24)
        self.ax.set_ylabel('RGB Intensity', fontsize=24)
        self.ax.set_title('Live RGB Intensity Plot', fontsize=32)
        self.ax.grid(False)
        self.line_r, = self.ax.plot([], [], color='#E69F00', marker='o', markersize=6, linestyle='-', label='Red')
        self.line_g, = self.ax.plot([], [], color='#009E73', marker='^', markersize=6, linestyle='-', label='Green')
        self.line_b, = self.ax.plot([], [], color='#56B4E9', marker='s', markersize=6, linestyle='-', label='Blue')
        self.ax.legend(fontsize=18, loc='center left', bbox_to_anchor=(1.02, 0.5), borderaxespad=0.)
        self.canvas = FigureCanvasAgg(self.fig)
        self.fig.tight_layout(rect=[0, 0, 0.85, 1])

    def start_capture(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")

        start_time = time.time()
        
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.current_frame = frame.copy()
                
                # Display RGB values on the frame
                roi = frame[self.y:self.y+self.h, self.x:self.x+self.w]
                avg_rgb = np.mean(roi, axis=(0, 1)).astype(int)
                b, g, r = avg_rgb
                
                # Overlay RGB text
                cv2.putText(frame, f"R: {r}, G: {g}, B: {b}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.rectangle(frame, (self.x, self.y), (self.x+self.w, self.y+self.h), (0, 255, 0), 2)
                
                # Update plot data
                current_time = time.time() - start_time
                self.time_data.append(current_time)
                self.r_data.append(r)
                self.g_data.append(g)
                self.b_data.append(b)
                
                # Update the plot
                self.line_r.set_data(self.time_data, self.r_data)
                self.line_g.set_data(self.time_data, self.g_data)
                self.line_b.set_data(self.time_data, self.b_data)
                self.ax.relim()
                self.ax.autoscale_view()
                self.canvas.draw()
                plot_img = np.array(self.canvas.renderer.buffer_rgba())
                plot_img = cv2.cvtColor(plot_img, cv2.COLOR_RGBA2BGR)
                
                # Resize plot to match camera frame height
                frame_height = frame.shape[0]
                plot_img = cv2.resize(plot_img, (int(plot_img.shape[1] * frame_height / plot_img.shape[0]), frame_height))
                
                # Show camera feed and plot side by side
                combined = np.hstack((frame, plot_img))
                cv2.imshow('Camera Feed + Live Plot', combined)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            time.sleep(0.02)

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
            time.sleep(0.2)
        
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