# -*- encoding:utf-8 -*-
import sys
import os
import time
import argparse
import math 
import cv2
import asyncio


# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))

from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper


HOST = "192.168.0.2"
PORT = 30003

async def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    gripper=RobotiqGripper()
    gripper.connect("192.168.0.2", 63352)

    new_home = [1.3348536491394043, -1.6144734821715296, 1.5730488936053675, -1.5615404548919578, -1.5539191404925745, -0.2927349249469202]
    vial_pickup_0 = [1.0490845441818237, -1.2347015899470826, 1.8862054983722132, -2.2256490192809046, -1.5525544325457972, 1.0632829666137695]
    vial_plate_intermediate = [1.1170587539672852, -1.4987735611251374, 1.561568562184469, -1.6459490261473597, -1.552575413380758, 1.0632418394088745]
    stirer_intermediate = [1.3536285161972046, -1.5596089049107213, 1.9042213598834437, -1.9661885700621546, -1.5563834349261683, -0.28846770921816045]
    stirrer_position = [1.3533833026885986, -1.4901131105474015, 1.9040244261371058, -1.9773227177061976, -1.5557358900653284, -0.28849822679628545]
    camera_position = [1.5405631065368652, -1.9327041111388148, 2.2914238611804407, -1.9269162617125453, -1.5510247389422815, -0.29272157350649053]
    end_plate_intermediate_0 = [1.6996548175811768, -1.1775085192969819, 1.7128971258746546, -2.111119409600729, -1.5870631376849573, -0.2889450232135218]
    end_plate_0 = [1.6991523504257202, -1.1309567254832764, 1.7128971258746546, -2.1226536236205042, -1.587397877370016, -0.28891116777528936]

  
    def goto(pos):
        robot.move_joint_list(pos, 0.7, 0.5, 0.02)

    def open_gripper():
        gripper.move(0,125,125) # Open Gripper

    def close_gripper():
        gripper.move(255,125,125) # Close Gripper

    # async def open_camera():
    #     cam = cv2.VideoCapture(0)
    #     cv2.namedWindow("test")
    #     img_counter = 0
    #     while True:
    #         ret, frame = cam.read()
    #         if not ret:
    #             print("failed to grab frame")
    #             break
    #         cv2.imshow("test", frame)
        
    #         k = cv2.waitKey(1)
    #         if k%256 == 27:
    #         #ESC pressed
    #             print("Escape hit , closing...")
    #             break

    #         elif k%256 ==32:
    #         #SPACE pressed
    #             img_name = "opencv_frame_{}.png".format(img_counter)
    #             cv2.imwrite(img_name, frame)
    #             print("{} written!".format(img_name))
    #             img_counter +=1
    #         cam.release
    #     cv2.destroyAllWindows()   
 
    goto(new_home)
    open_gripper()

    goto(vial_pickup_0)
    close_gripper()

    goto(vial_plate_intermediate)

    goto(new_home)

    goto(stirer_intermediate)
    goto(stirrer_position)
    open_gripper()
    goto(new_home)
    time.sleep(5)
    goto(stirrer_position)
    close_gripper()
    goto(new_home)

    goto(camera_position)
    # await open_camera()
    time.sleep(5)
    # add an if or else statement depending on camera run to go to end or stirrer
    # also add if stirred 3 times then go to failed section

    goto(new_home)
    goto(end_plate_intermediate_0)
    goto(end_plate_0)
    open_gripper()
    goto(new_home)

def degreestorad(list):
     for i in range(6):
          list[i]=list[i]*(math.pi/180)
     return(list)

if __name__ == '__main__':
     main()