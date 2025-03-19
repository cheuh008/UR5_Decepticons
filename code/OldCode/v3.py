import cv2
import numpy as np

# Function to select ROI
def select_roi(frame):
    roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select ROI")
    return roi

# Function to check if the color is close to (170, 170, 170)
def is_colorless(rgb_values):
    threshold = 10
    target_color = np.array([170, 170, 170])
    return np.all(np.abs(rgb_values - target_color) < threshold)

# Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Capture a single frame to select ROI
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame.")
    cap.release()
    exit()

# Let the user select the ROI
roi = select_roi(frame)
x, y, w, h = roi

roi_frame = frame[y:y+h, x:x+w]

print(x, y, w, h)
print (roi_frame)

# # Main loop to continuously extract RGB values from the ROI
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Could not read frame.")
#         break

#     # Extract the ROI
#     roi_frame = frame[y:y+h, x:x+w]

#     # Calculate the average RGB value in the ROI
#     average_rgb = np.mean(roi_frame, axis=(0, 1))

#     # Display the average RGB value
#     print(f"Average RGB: {average_rgb}")

#     # Check if the color is close to (170, 170, 170)
#     if is_colorless(average_rgb):
#         print("Colorless detected. Stopping...")
#         break

#     # Display the frame with the ROI
#     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     cv2.imshow("Camera", frame)

#     # Break the loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()