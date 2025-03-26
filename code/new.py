# =============================================================================
# region Imports
# =============================================================================
import cv2
import sys
import os
import json
import time
import threading
import numpy as np

# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))

from utils.UR_Functions import URfunctions as URControl
from utils.ika_serial_driver import IKADriver
from robotiq.robotiq_gripper import RobotiqGripper
from camv2 import process_image

# =============================================================================
# region Constants
# =============================================================================

HOST = "192.168.0.2"
PORT = 30003
ITERATIONS = 4 # index starts at 0 
STIR_TIME = 2

# stir = IKADriver('ttyACM0')
# stir.setStir(15000)
# stir.startStir()
# stir.stopStir()

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
# region Main Work
# =============================================================================

def main():
    """ Executes the workflow for (i) vial(s) """ 
    for i in range(ITERATIONS): 
        print(f"Processing iteration {i}")
        ungrab() 
        move_to('start')
        move_to('pickup', i)
        grab()
        move_to('start')
        move_to('stir_interm')
        move_to('stirer')
        ungrab()
        move_to('stir_interm')
        
        print(f"Waiting for {STIR_TIME} seconds")
        time.sleep(STIR_TIME)
        move_to('stirer')
        grab()
        move_to('stir_interm')
        move_to('camera')
        process_image(i)
        move_to('cam_interm')
        move_to('end_interm', i)
        move_to('end', i)
        ungrab()
        move_to('home')
        print(f"Iteration {i} complete")
        print("Workflow End")
    


 
# =============================================================================
# region Main
# =============================================================================

if __name__ == '__main__':
    main()

    # ungrab() 
    # grab()
    # i = 0
    # move_to('start')
    # move_to('pickup', i)
    # move_to('stir_interm')
    # move_to('stirer')
    # move_to('camera')
    # move_to('cam_interm')
    # move_to('end_interm', 0)
    # move_to('end', i)
