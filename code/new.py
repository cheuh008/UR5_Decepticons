
import sys, os, json, math, threading, cv2, time 
import numpy as np

# Add the directory containing rexiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))

from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper
from camera import process_image

with open("positions.json", "r") as json_file:
    POSITIONS = json.load(json_file)

HOST = "192.168.0.2"
PORT = 30003
MAX_ROUNDS = 2
SLEEP_TIME = 2
ITERATIONS = 4


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

def check():
    """Workflow Loop, returns True for colour change else Fasle """
    move_to(POSITIONS['stir_interm'])
    move_to(POSITIONS['stirer'])
    ungrab()

    move_to(POSITIONS['home'])
    time.sleep(SLEEP_TIME)

    move_to(POSITIONS['stirer'])
    grab()
    move_to(POSITIONS['home'])
    move_to(POSITIONS['camera'])

    process_image()

    return False

def workflow(i):

    ungrab()
    move_to(POSITIONS['home'])
    move_to((POSITIONS['pickup'])[i])
    grab()

    move_to(POSITIONS['VP_interm'])
    move_to(POSITIONS['home'])

    rounds = 0
    colour_change = False 
    colour_change = check()
    
    while not colour_change and rounds < MAX_ROUNDS:
        check()
        rounds += 1
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


def main():
    """Main execution function."""
    
    for i in range(ITERATIONS):
        print(f"Processing iteraation {i}")
        workflow(i)

    print("All vials processed. Exiting program.")

def degreestorad(list):
    for i in range(6):
        list[i] = list[i] * (math.pi / 180)
    return list

if __name__ == '__main__':
    main()