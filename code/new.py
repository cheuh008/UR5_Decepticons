
import sys, os, json, math, asyncio, threading, cv2
import numpy as np

# Add the directory containing rexiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'rexiq'))

from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper
from camera import colour_change_detector, capture_image, open_camera

iterations = 4
with open("positions.json", "r") as json_file:
    POSITIONS = json.load(json_file)

# Color detection parameters
UPPER_BLUE = np.array([140, 255, 255])  
LOWER_BLUE = np.array([100, 50, 50])  

HOST = "192.168.0.2"
PORT = 30003
MAX_ROUNDS = 2

rex = URControl(ip=HOST, port=PORT)
gripper = RobotiqGripper()
gripper.connect(HOST, 63352)

def move_to(pos):
    """Moves the rex to the specified position."""
    rex.move_joint_list(pos, 0.7, 0.5, 0.05)

def grab():
    """Close the gripper """
    gripper.move(255, 125, 125)

def ungrab():
    """Opens the gripper """
    gripper.move(0, 125, 125)

async def check():
    # Loop?
    move_to(POSITIONS['stir_interm'])
    move_to(POSITIONS['stirer'])
    ungrab()

    move_to(POSITIONS['home'])
    await asyncio.sleep(5)

    move_to(POSITIONS['stirer'])
    grab()
    move_to(POSITIONS['home'])
    move_to(POSITIONS['camera'])

    return colour_change_detector

async def workflow(i):

    # Start
    ungrab()
    move_to(POSITIONS['home'])
    move_to(POSITIONS['pickup'][i])
    grab()

    move_to(POSITIONS['VP_interm'][i])
    move_to(POSITIONS['home'])

    rounds = 0
    colour_change = False 
    colour_change = await check()
    
    while not colour_change or rounds < MAX_ROUNDS:
        await check()
        await asyncio.sleep(5)
        if colour_change:
            print("Yay")
        else:
            print(rounds)
            print("timeout?")
    
    move_to(POSITIONS['home'])
    move_to(POSITIONS['end_interm'][i])
    move_to(POSITIONS['end'][i])
    ungrab()
    move_to(POSITIONS['home'])
    print("Workflow End")



async def main():
    """Main execution function."""
    threading.Thread(target=asyncio.run, args=(open(),)).start()

    for i in range(iterations):
        print(f"Processing iteraation {i}")
        await workflow(i)

    print("All vials processed. Exiting program.")

def degreestorad(list):
    for i in range(6):
        list[i] = list[i] * (math.pi / 180)
    return list

if __name__ == '__main__':
    asyncio.run(main())