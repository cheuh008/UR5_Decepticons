# =============================================================================
# region Imports
# =============================================================================
import cv2
import sys
import os
import json
import time
import numpy as np
import threading

# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))

from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper
from camv2 import process_image
from typing import Optional

# =============================================================================
# region Constants
# =============================================================================

HOST = "192.168.0.2"
PORT = 30003
ITERATIONS = 4

# cap = cv2.VideoCapture(0)  # 0 is the default camera
# x, y, w, h = 100, 100, 50, 50  # Example: a 50x50 square at (100, 100)

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

def check(i = 0, slp = 5, tries= 2, colour_change = False, round = 0,):
    """ Colour Change detector Loop 

    Parameters:
        tries (int): The number of tries (iterations) the loop will run. Default is 2.

        slp (int or float): The number of seconds to wait (sleep) between each check. Default is 5 seconds.
        colour_change (bool): A flag indicating whether a color change has occurred. 
                            The loop will stop if this is True. Default is False.
        round (int): Starting round / iterations. Default is 2.

    Returns: None
    """
    
    while not colour_change and round <= tries:
        # Vial Drop Off
        move_to('stir_interm')
        move_to('stirer')
        ungrab()
        # Vial Waititing
        move_to('stir_interm')
        time.sleep(slp)
        print(f"Wating for {slp} seconds")
        # Vial Pickup
        move_to('stirer')
        grab()
        move_to('stir_interm')
        # Camera AI Logic 
        move_to('camera')

        process_image(i)
        round += 1     
        # detector loop break
        if colour_change:
            print("Yay")
            return
        else:
            print(f"No Colour Change Detected, Attempt {round}/{tries}")

    print("Timeout: Max Tries. Poceeding to end")        
    return 

def main():
    """ Executes the workflow for a (i) vial(s) """ 

# Open the camera
    # i = 0 debug override default 4
    for i in range(ITERATIONS):
        print(f"Processing iteraation {i}")
        ungrab() 
        move_to('start')
        move_to('pickup', i)
        grab()
        move_to('start')

        # Debug Overide
        check(i, slp=0, tries=0)    

        move_to('end_interm', i)
        move_to('end', i)
        ungrab()
        move_to('home')
        print("Workflow End")
        #debug(i)

    print("Timeout: Max Tries. Poceeding to end")        
 

# =============================================================================
# region Main
# =============================================================================

if __name__ == '__main__':

    
    # main()
    # print("Workflow End")

    # Debug    
    i = 0
    # ungrab()
    move_to('start')
    # move_to('pickup', i)
    # grab()
    # move_to('start')
    # move_to('stir_interm')
    # move_to('stirer')
    # ungrab()
    # move_to('stir_interm')
    # # time.sleep(2)
    # move_to('stirer')
    # grab()
    # move_to('stir_interm')
    move_to('camera')
    process_image(i)
    # move_to('end_interm', i)
    # move_to('end', i) 
    # ungrab()
    # move_to('home')
    # print("Workflow End")

