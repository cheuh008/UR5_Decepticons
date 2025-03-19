import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

def monitor_reaction():
    # Initialize camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Define ROI (Region of Interest) for the reaction
    x, y, w, h = 200, 150, 100, 100  # Adjust these values based on your setup

    # Lists to store intensity and time data
    intensities = []
    timestamps = []

    try:
        start_time = time.time()
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Extract ROI
            roi = frame[y:y+h, x:x+w]

            # Convert ROI to grayscale (to measure intensity)
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            # Calculate average intensity of the ROI
            average_intensity = np.mean(gray_roi)

            # Record intensity and timestamp
            current_time = time.time() - start_time
            intensities.append(average_intensity)
            timestamps.append(current_time)

            # Display the frame with ROI
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Intensity: {average_intensity:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Reaction Monitoring', frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release the camera and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        # Plot reaction kinetics
        plt.plot(timestamps, intensities, label="Intensity (Blue Color)")
        plt.xlabel("Time (s)")
        plt.ylabel("Intensity")
        plt.title("Reaction Kinetics: Methylene Blue with Perchlorates")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    monitor_reaction()