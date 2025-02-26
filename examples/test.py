import sys
import os
import time
import argparse
import math 
import cv2
import asyncio
import threading

# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))

from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper

new_home = [1.3348536491394043, -1.6144734821715296, 1.5730488936053675, -1.5615404548919578, -1.5539191404925745, -0.2927349249469202]
vial_pickup_0 = [1.0490845441818237, -1.2347015899470826, 1.8862054983722132, -2.2256490192809046, -1.5525544325457972, 1.0632829666137695] # 0
# [1.0636930465698242, -1.1893766087344666, 1.8074825445758265, -2.1872321567931117, -1.5328400770770472, 1.0603461265563965] # 1
# [1.114319086074829, -1.1392197769931336, 1.7042668501483362, -2.1286589107909144, -1.5964182058917444, 1.5022380352020264] # 2
# [1.114319086074829, -1.1392197769931336, 1.7042668501483362, -2.1286589107909144, -1.5964182058917444, 1.5022380352020264] # 3
# [1.108981728553772, -1.2619552177241822, 1.9085477034198206, -2.203841825524801, -1.5254181067096155, 1.0677990913391113] # 4
# [1.1437020301818848, -1.2171921294978638, 1.85162860551943, -2.2235738239684046, -1.5547211805926722, 1.8110084533691406] # 5
# [1.1509544849395752, -1.1585918825915833, 1.7517932097064417, -2.1524983845152796, -1.526743237172262, 1.8083500862121582] # 6
# vial_pickup_0 = [1.177856206893921, -1.1080926221660157, 1.682671372090475, -2.15537752727651, -1.541666332875387, 1.8952510356903076] # 7
vial_plate_intermediate = [1.1170587539672852, -1.4987735611251374, 1.561568562184469, -1.6459490261473597, -1.552575413380758, 1.0632418394088745]
stirer_intermediate = [1.3536285161972046, -1.5596089049107213, 1.9042213598834437, -1.9661885700621546, -1.5563834349261683, -0.28846770921816045]
stirrer_position = [1.3533833026885986, -1.4901131105474015, 1.9040244261371058, -1.9773227177061976, -1.5557358900653284, -0.28849822679628545]
camera_position = [1.5405631065368652, -1.9327041111388148, 2.2914238611804407, -1.9269162617125453, -1.5510247389422815, -0.29272157350649053]
end_plate_intermediate_0 = [1.6700143814086914, -1.1888567966273804, 1.689509693776266, -2.0677505932249964, -1.5356534163104456, -0.2683914343463343]
# end_plate_intermediate_0 = [1.650180459022522, -1.11443583786998, 1.666863743458883, -2.122789045373434, -1.4902318159686487, -0.27125436464418584] # 2
# end_plate_intermediate_0 = [1.6799054145812988, -1.0675780934146424, 1.5524652639972132, -2.053753515283102, -1.5616729895221155, -0.2901495138751429] # 3
# end_plate_intermediate_0 = [1.668087124824524, -1.0212004345706482, 1.4788315931903284, -2.0429655514159144, -1.541999642048971, -0.29016143480409795] # 4
end_plate_0 = [1.6830980777740479, -1.1380524200252076, 1.7275798956500452, -2.1436130009093226, -1.5491254965411585, 1.0660600662231445]
# end_plate_0 = [1.6921695470809937, -1.09274776399646, 1.6587136427508753, -2.1459037266173304, -1.5800240675555628, 3.6227357387542725] # End_2
# end_plate_0 = [1.6935619115829468, -1.0261858862689515, 1.5369141737567347, -2.0552860699095667, -1.5954092184649866, 4.359703063964844] # End_3
# end_plate_0 =  [1.6784923076629639, -0.9912229341319581, 1.4889605681048792, -2.076402326623434, -1.5669849554644983, 4.669535160064697] # End_4

HOST = "192.168.0.2"
PORT = 30003

async def open_camera():
    
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)
    
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

        elif k % 256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
    cam.release()
    cv2.destroyAllWindows()

async def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    gripper = RobotiqGripper()
    gripper.connect("192.168.0.2", 63352)
    camera_thread = threading.Thread(target=asyncio.run, args=(open_camera(),))
    camera_thread.start()

    def goto(pos):
        robot.move_joint_list(pos, 0.7, 0.5, 0.05)

    def open_gripper():
        gripper.move(0, 125, 125)  # Open Gripper

    def close_gripper():
        gripper.move(255, 125, 125)  # Close Gripper


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
    await asyncio.sleep(5)
    goto(stirrer_position)
    close_gripper()
    goto(new_home)

    goto(camera_position)
    # Run camera in a separate thread

    await asyncio.sleep(5)
    # add an if or else statement depending on camera run to go to end or stirrer
    # also add if stirred 3 times then go to failed section

    goto(new_home)
    goto(end_plate_intermediate_0)
    goto(end_plate_0)
    open_gripper()
    goto(new_home)

def degreestorad(list):
    for i in range(6):
        list[i] = list[i] * (math.pi / 180)
    return list

if __name__ == '__main__':
    asyncio.run(main())