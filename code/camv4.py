import cv2
import os
import numpy as np
import time
import csv
import threading
from collections import deque
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt

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
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('RGB Intensity')
        self.ax.set_title('Live RGB Intensity Plot')
        self.ax.grid(True)
        self.line_r, = self.ax.plot([], [], 'r-', label='Red')
        self.line_g, = self.ax.plot([], [], 'g-', label='Green')
        self.line_b, = self.ax.plot([], [], 'b-', label='Blue')
        self.ax.legend()
        self.canvas = FigureCanvasAgg(self.fig)

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
        # (Your existing code for saving data)
        pass

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