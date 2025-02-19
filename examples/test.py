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

    new_home = [1.0294861793518066, -1.4273227763227005, 1.4040244261371058, -1.551843050201871, -1.5698121229754847, 0.00013137006317265332]
    vial_pickup = [1.0490845441818237, -1.2347015899470826, 1.8862054983722132, -2.2256490192809046, -1.5525544325457972, 1.0632829666137695]
    vial_plate_intermediate = [1.1170587539672852, -1.4987735611251374, 1.561568562184469, -1.6459490261473597, -1.552575413380758, 1.0632418394088745]
    plate_pickup = []
    plate_wait = []
    plate_end_intermediate = []
    end_dropoff = []

    def goto(pos):
        robot.move_joint_list(pos, 0.7, 0.5, 0.02)

    def open_gripper():
        gripper.move(0,125,125) # Open Gripper

    def close_gripper():
        gripper.move(255,125,125) # Close Gripper
     
    goto(new_home)
    open_gripper()

    goto(vial_pickup)
    close_gripper()

    goto(vial_plate_intermediate)

    goto(plate_pickup)
    open_gripper()

    goto(plate_wait)
    goto(plate_pickup)
    close_gripper()
    goto(plate_wait)

    goto(plate_end_intermediate)
    goto(end_dropoff)
    open_gripper()

    # #robot.go_home()
    # # Home
    # joint_state=degreestorad([93.77,-89.07,89.97,-90.01,-90.04,0.0])
    # robot.move_joint_list(joint_state, 0.5, 0.5, 0.02)


def degreestorad(list):
     for i in range(6):
          list[i]=list[i]*(math.pi/180)
     return(list)

if __name__ == '__main__':
     main()