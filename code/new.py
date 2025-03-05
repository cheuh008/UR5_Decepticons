# =============================================================================
# region Imports
# =============================================================================
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
from camera import process_image
from typing import Optional

# =============================================================================
# region Constants
# =============================================================================

file_path = os.path.join(current_dir, 'data', 'positions.json')
with open(file_path, "r") as json_file:
    POSITIONS = json.load(json_file)

HOST = "192.168.0.2"
PORT = 30003
MAX_ROUNDS = 2
SLEEP_TIME = 2
ITERATIONS = 4

Rex = URControl(ip=HOST, port=PORT)
gripper = RobotiqGripper()
gripper.connect(HOST, 63352)

# =============================================================================
# region Helper Function
# =============================================================================

def move_to(key: str, i: Optional[int] = None) -> None:
    """Moves Robot Arm (Rex) to the specified position."""
    pos = POSITIONS[key][i] if i else POSITIONS[key]
    Rex.move_joint_list(pos, 0.7, 0.5, 0.05)
    print(f"Moving to {key}"  + (f" (for vial: {i})" if i else ""))

def grab() -> None:
    """Close the gripper """
    print("Closing Gripper, Grabbing Vial")
    gripper.move(255, 125, 125)

def ungrab() -> None:
    """Opens the gripper """
    print("Opening Gripper, Releasing Vial")
    gripper.move(0, 125, 125)

# =============================================================================
# region Colour Checker
# =============================================================================

def check() -> bool:
    """ 
    Executes a workflow loop to check for color change 
    Returns: 
        bool: True if colour change detected, else False
    """

    # Taking Vial to Stirer (Shaker)
    move_to('stir_interm')
    move_to('stirer')
    ungrab()

    # Waiting 
    move_to('home')
    print(f"Wating for {SLEEP_TIME} seconds")
    time.sleep(SLEEP_TIME)
    move_to('stirer')
    grab()
    
    # Taking Vial to Camera
    move_to('home')
    move_to('camera')
    process_image()

    return False # Placeholder, replace with actual color change detection logic

# =============================================================================
# region Iter Workflow
# =============================================================================

def workflow(i):
    """ 
    Executes the workflow for a single vial
    
    Args: 
        i (int): The iteration/vial number.
    """ 

    # prep, opening gripper for pick up
    ungrab() 
    move_to('home')
    move_to('pickup', i)
    grab()

    move_to('VP_interm')
    move_to('home')

    rounds = 0 # time out tracker
    colour_change = False 
    colour_change = check()
    
    while not colour_change and rounds <= MAX_ROUNDS:
        check()
        rounds += 1
        if colour_change:
            print("Yay")
        elif rounds == MAX_ROUNDS:
            print("Max Round Timeout, Ending Loop")
        else:
            print(f"No Colour Change Detected, Attempt {round}/{MAX_ROUNDS}")
    
    move_to('home')
    move_to('end_interm', i)
    move_to('end', i)
    ungrab()
    move_to('home')
    print("Workflow End")

# =============================================================================
# region Main Iter 
# =============================================================================

def main() -> None:
    """Main execution function."""
    
    for i in range(ITERATIONS):
        print(f"Processing iteraation {i}")
        workflow(i)

    print("All vials processed. Exiting program.")


# =============================================================================
# region Main
# =============================================================================

if __name__ == '__main__':
    main()