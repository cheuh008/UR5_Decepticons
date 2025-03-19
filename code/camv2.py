import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)  # 0 is the default camera
x, y, w, h = 267, 102, 72, 78

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        roi = frame[y:y+h, x:x+w]
        average_color = np.mean(roi, axis=(0, 1)).astype(int)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Timestamp: {timestamp}, ROI Color (BGR): {average_color}")
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw rectangle around ROI
        cv2.imshow('Camera Stream', frame)


finally:
    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()