# =============================================================================
# region Import
# =============================================================================

import cv2
import os
import numpy as np
import pandas as pd
from typing import Optional, Tuple

# =============================================================================
# region Capture Image
# =============================================================================

def capture_image(current_dir: str) -> Optional[Tuple[str, np.ndarray]]:
    """
    Captures, crops, and saves an image from the webcam.
        Args: current_dir (str)
        Returns: Tuple[str, np.ndarray] or None if an error occurs.
    """
    save_path = os.path.join(current_dir, 'data', 'images')
    os.makedirs(save_path, exist_ok=True)
    
    try:
        # Try to open camera and read frame
        cam = cv2.VideoCapture(0)
        if not cam.isOpened(): 
            raise RuntimeError("Could not open camera.")
        
        ret, frame = cam.read()
        if not ret or frame is None: 
            raise ValueError("Failed to capture image.")
    
        # Cropping image to vial area
        h, w, _ = frame.shape
        crop_width, crop_height = w // 4, h // 4
        start_x, start_y = (w // 2) + (w // 8) - (crop_width // 2), h // 8
        cropped_image = frame[start_y:start_y + crop_height, start_x:start_x + crop_width]

        if cropped_image.size == 0: 
            raise ValueError("Cropping failed.")
    
        # Determine next available file name
        existing_files = [f for f in os.listdir(save_path) if f.startswith("img_") and f.endswith(".jpg")]
        next_number = max((int(f.split("_")[-1].split(".")[0]) for f in existing_files), default=-1) + 1
        image_path = os.path.join(save_path, f"img_{next_number}.jpg")

        # Save cropped image
        cv2.imwrite(image_path, frame )#cropped_image)
        print(f"Saved: {image_path}")
        return image_path, cropped_image

    except Exception as e:
        print(f"Error capturing image: {e}")
        return None

    finally:
        cam.release()
        cv2.destroyAllWindows()


# =============================================================================
# region Extract RGB
# =============================================================================

def extract_rgb(current_dir: str, image_path: str, image: np.ndarray) -> None:
    """
    Extracts and saves RGB values from the image.
        Args: current_dir (str), image_path (str), image (np.ndarray): The image array.
    """

    try:
        # Convert image to RGB and compute average color
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        avg_color = np.mean(image_rgb, axis=(0, 1))  
        r, g, b = map(int, avg_color)
        csv_path = os.path.join(current_dir, 'data', 'RGB_values.csv')      

        # Save RGB values to CSV file
        sample_id = os.path.basename(image_path).split("_")[-1].split(".")[0]
        
        df = pd.DataFrame([[sample_id, r, g, b]], columns=["Sample_ID", "Red", "Green", "Blue"])
        df.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)
        print(f"Saved RGB to {csv_path}")

    except Exception as e:
        print(f"Error extracting RGB: {e}")

# =============================================================================
# region Main Process Image
# =============================================================================

def process_image() -> None:
    """Captures image and extracts RGB."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Capture and process image
    try:
        result = capture_image(current_dir)
        if result:
            extract_rgb(current_dir, *result)
    except Exception as e:
        print(f"Skipping RGB extraction: {e}")

# =============================================================================
# region Main 
# =============================================================================
if __name__ == "__main__":
    process_image()