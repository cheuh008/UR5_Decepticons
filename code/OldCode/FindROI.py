import cv2

# Function to select ROI
def select_roi(frame):
    roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select ROI")
    return roi

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame.")
    cap.release()
    exit()

# Let the user select the ROI
roi = select_roi(frame)
x, y, w, h = roi

roi_frame = frame[y:y+h, x:x+w]

print(roi)
cap.release()
cv2.destroyAllWindows()