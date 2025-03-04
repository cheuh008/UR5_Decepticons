
import sys, os, json, math, asyncio, threading, cv2
import numpy as np

# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))

from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper
from camera import open, box, detect

iterations = 4
with open("positions.json", "r") as json_file:
    POSITIONS = json.load(json_file)

# Color detection parameters
UPPER_BLUE = np.array([140, 255, 255])  
LOWER_BLUE = np.array([100, 50, 50])  

HOST = "192.168.0.2"
PORT = 30003

def move_to(robot, pos):
    """Moves the robot to the specified position."""
    robot.move_joint_list(pos, 0.7, 0.5, 0.05)

def grab(gripper, close: bool):
    """Controls the gripper (True = close, False = open)."""
    gripper.move(255 if close else 0, 125, 125)

async def main():
    """Main execution function."""
    robot = URControl(ip=HOST, port=PORT)
    gripper = RobotiqGripper()
    gripper.connect(HOST, 63352)
    threading.Thread(target=asyncio.run, args=(open(),)).start()

    for i in range(iterations):
        for key, pos in POSITIONS.items():
            position = pos[i] if key in ["pickup", "end_interm", "end"] else pos
            move_to(robot, position)
            grab(gripper, close=(key in ["pickup", "stirrer"]))
            await asyncio.sleep(5) if key == "camera" else None

        ret, frame = cv2.VideoCapture(0).read()

        if ret and detect(frame, LOWER_BLUE, UPPER_BLUE):
            print("Color change detected. Moving to end position.")
            move_to(robot, POSITIONS["end"])
            grab(gripper, close=False)
        else:
            print("No color change detected. Returning to stirrer.")
            move_to(robot, POSITIONS["stirrer"])
            grab(gripper, close=True)
        move_to(robot, POSITIONS["home"])

    print("All vials processed. Exiting program.")

def degreestorad(list):
    for i in range(6):
        list[i] = list[i] * (math.pi / 180)
    return list

if __name__ == '__main__':
    asyncio.run(main())