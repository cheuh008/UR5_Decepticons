# =============================================================================
# region Imports
# =============================================================================
import cv2
import sys
import os
import json
import time
import numpy as np

# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))

from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper
from camv2 import process_image

# =============================================================================
# region Constants
# =============================================================================

HOST = "192.168.0.2"
PORT = 30003
ITERATIONS = 3 # index starts at 0 
STIR_TIME = 2

Rex = URControl(ip=HOST, port=PORT)
gripper = RobotiqGripper()
gripper.connect(HOST, 63352)


file_path = os.path.join(current_dir, 'data', 'positions.json')
with open(file_path, "r") as json_file:
    POSITIONS = json.load(json_file)

# =============================================================================
# region Helper Function
# =============================================================================

def move_to(key: str, i = None):
    """Moves Robot Arm (Rex) to the specified position."""

    pos = POSITIONS[key] if i is None else POSITIONS[key][i]
    Rex.move_joint_list(pos, 1, 0.75, 0.05)
    print(f"Moving to {key}"  + (f" (for vial: {i})" if i else ""))

def grab():
    """Close the gripper """
    print("Closing Gripper, Grabbing Vial")
    gripper.move(255, 125, 125)

def ungrab():
    """Opens the gripper """
    print("Opening Gripper, Releasing Vial")
    gripper.move(0, 125, 125)

# =============================================================================
# region Colour Checker
# =============================================================================



def main():
    """ Executes the workflow for (i) vial(s) """ 

    for i in range(ITERATIONS): 
        print(f"Processing iteraation {i}")
        ungrab() 
        move_to('start')
        move_to('pickup', i)
        grab()
        move_to('start')

        move_to('stir_interm')
        move_to('stirer')
        ungrab()
        # Vial Waititing
        move_to('stir_interm')
        time.sleep(STIR_TIME)
        print(f"Wating for {STIR_TIME} seconds")
        # Vial Pickup
        move_to('stirer')
        grab()
        move_to('stir_interm')
        # Camera AI Logic 
        move_to('camera')
        process_image(i)
        move_to('end_interm', i)
        move_to('end', i)
        ungrab()
        move_to('home')
        print("Workflow End")

 

# =============================================================================
# region Main
# =============================================================================

if __name__ == '__main__':
    main()
    print("Workflow End")
