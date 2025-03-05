import sys
import os
import json
import math
import asyncio
import cv2
import numpy as np

# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))

from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper
from camera import open_camera, box, detect

# Constants
HOST = "192.168.0.2"
PORT = 30003
UPPER_BLUE = np.array([140, 255, 255])
LOWER_BLUE = np.array([100, 50, 50])
ITERATIONS = 4
MAX_RETRIES = 2

# Load positions from JSON
with open("positions.json", "r") as json_file:
    POSITIONS = json.load(json_file)

class RobotController:
    def __init__(self, host, port):
        self.robot = URControl(ip=host, port=port)
        self.gripper = RobotiqGripper()
        self.gripper.connect(host, 63352)

    async def move_to(self, pos):
        """Moves the robot to the specified position."""
        self.robot.move_joint_list(pos, 0.7, 0.5, 0.05)

    def grab(self, close: bool):
        """Controls the gripper (True = close, False = open)."""
        self.gripper.move(255 if close else 0, 125, 125)


async def camera_ai() -> bool:
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame from camera.")
        raise ValueError

    if detect(frame, LOWER_BLUE, UPPER_BLUE):
        print("Color change detected.")
        return True  # Color change detected

    print(f"No color change detected.")
    return False  # 

async def process_workflow(rex, key, workflow, i):
    """Processes the workflow for a single vial."""

    index = ["vial_pickup", "end_interme", "vial_end"]
    position = workflow["coords"][i] if key in index else workflow["coords"]
    await rex.move_to(position)

    if workflow["grab"] is not None:
        rex.grab(workflow["grab"])

    if key == 'camera_position':
        global color_change
        color_change = await camera_ai()
    
    if key == 'camera_position' or key == 'home3':
        await asyncio.sleep(5)



async def process_vial(rex, iteration):
    """Processes json workflow in order."""
    retries = 0
    color_change = False

    for key, workflow in POSITIONS.items():
        # separate interior loop for loop workflow
        if key == "loop":
            while retries < MAX_RETRIES or not color_change:
                for steps, workflow in POSITIONS["loop"]:
                    await process_workflow(rex, steps, workflow, iteration)
                    retries += 1

        await process_workflow(rex, key, workflow, iteration)

async def main():
    """Main execution function."""
    rex = RobotController(HOST, PORT)
    open_camera()

    for i in range(ITERATIONS):
        await process_vial(rex, i)

    print("All vials processed. Exiting program.")

if __name__ == '__main__':
    asyncio.run(main())