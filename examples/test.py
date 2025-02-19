# -*- encoding:utf-8 -*-
import sys
import os
import time
import argparse
import math 

# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))

from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper


HOST = "192.168.0.2"
PORT = 30003


def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    gripper=RobotiqGripper()
    gripper.connect("192.168.0.2", 63352)

    # #robot.go_home()
    # # Home
    # joint_state=degreestorad([93.77,-89.07,89.97,-90.01,-90.04,0.0])
    # robot.move_joint_list(joint_state, 0.5, 0.5, 0.02)

    joint_state= [1.0294861793518066, -1.4273227763227005, 1.4040244261371058, -1.551843050201871, -1.5698121229754847, 0.00013137006317265332]
    robot.move_joint_list(joint_state, 0.5, 0.5, 0.02)
    gripper.move(0,125,125)     # Open Gripper
    
    # Position A: Above Vial Start
    joint_state = [1.0490845441818237, -1.2347015899470826, 1.8862054983722132, -2.2256490192809046, -1.5525544325457972, 1.0632829666137695]
    robot.move_joint_list(joint_state, 0.5, 0.5, 0.02)
    gripper.move(255,125,125)     # Close Gripper

    joint_state = [1.1170587539672852, -1.4987735611251374, 1.561568562184469, -1.6459490261473597, -1.552575413380758, 1.0632418394088745]
    robot.move_joint_list(joint_state, 0.5, 0.5, 0.02)

    # # Position C: Above Vial End - 
    # joint_state = [1.5515978336334229, -1.6546455822386683, 2.3073864618884485, -2.1558286152281703, -1.560286823903219, 1.2228846549987793]
    # robot.move_joint_list(joint_state, 0.5, 0.5, 0.02)
    

    # joint_state = [1.5160772800445557, -1.592754980126852, 2.3201831022845667, -2.270933767358297, -1.5024340788470667, 1.221303939819336]
    # robot.move_joint_list(joint_state, 0.5, 0.5, 0.02)
    # #FOR ROS  
    # joint_state = [0.0,-1.57,0.0,-1.57,0.0,0.0]
    # #robot.move_joint_list(joint_state, 0.5, 0.5, 0.02)

def degreestorad(list):
     for i in range(6):
          list[i]=list[i]*(math.pi/180)
     return(list)

if __name__ == '__main__':
     main()