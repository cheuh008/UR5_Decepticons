# -*- encoding:utf-8 -*-
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
camera_thread = threading.Thread(target=asyncio.run, args=(open_camera(),))
camera_thread.start()

async def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    gripper = RobotiqGripper()
    gripper.connect("192.168.0.2", 63352)

    new_home = [1.3348536491394043, -1.6144734821715296, 1.5730488936053675, -1.5615404548919578, -1.5539191404925745, -0.2927349249469202]
    vial_pickup_0 = [1.0654441118240356, -1.219952182178833, 1.8635318914996546, -2.2141744099059046, -1.5864689985858362, -0.29245120683778936] # 0
    vial_pickup_1 = [1.0669639110565186, -1.171164945965149, 1.791931454335348, -2.179608007470602, -1.5372656027423304, -0.48901683488954717] # 1
    # [1.114319086074829, -1.1392197769931336, 1.7042668501483362, -2.1286589107909144, -1.5964182058917444, 1.5022380352020264] # 2
    # [1.114319086074829, -1.1392197769931336, 1.7042668501483362, -2.1286589107909144, -1.5964182058917444, 1.5022380352020264] # 3
    # [1.108981728553772, -1.2619552177241822, 1.9085477034198206, -2.203841825524801, -1.5254181067096155, 1.0677990913391113] # 4
    # [1.1437020301818848, -1.2171921294978638, 1.85162860551943, -2.2235738239684046, -1.5547211805926722, 1.8110084533691406] # 5
    # [1.1509544849395752, -1.1585918825915833, 1.7517932097064417, -2.1524983845152796, -1.526743237172262, 1.8083500862121582] # 6
    # vial_pickup_0 = [1.177856206893921, -1.1080926221660157, 1.682671372090475, -2.15537752727651, -1.541666332875387, 1.8952510356903076] # 7
    vial_plate_intermediate = [1.1170587539672852, -1.4987735611251374, 1.561568562184469, -1.6459490261473597, -1.552575413380758, 1.0632418394088745]
    stirer_intermediate = [1.3532801866531372, -1.5073005569032212, 1.868021313344137, -1.9257518253722132, -1.5573704878436487, -0.2886012236224573]
    stirrer_position = [1.353271722793579, -1.4905654725483437, 1.9034879843341272, -1.9808117351927699, -1.5576022307025355, -0.2884419600116175]
    camera_position = [1.5405631065368652, -1.9327041111388148, 2.2914238611804407, -1.9269162617125453, -1.5510247389422815, -0.29272157350649053]
    end_plate_intermediate_0 = [1.6912245750427246, -1.1685702365687867, 1.7128618399249476, -2.1300579510130824, -1.56842548051943, -0.28793365160097295]
    end_plate_intermediate_1 = [1.6643126010894775, -1.1203327637961884, 1.644454304371969, -2.10503687481069, -1.52537709871401, 0.014248140156269073] # 2
    # end_plate_intermediate_0 = [1.6799054145812988, -1.0675780934146424, 1.5524652639972132, -2.053753515283102, -1.5616729895221155, -0.2901495138751429] # 3
    # end_plate_intermediate_0 = [1.668087124824524, -1.0212004345706482, 1.4788315931903284, -2.0429655514159144, -1.541999642048971, -0.29016143480409795] # 4
    end_plate_0 = [1.6912126541137695, -1.138682798748352, 1.7376397291766565, -2.18473019222402, -1.5686395804034632, -0.2877724806415003]
    end_plate_1 = [1.664297103881836, -1.09848044932399, 1.6634991804706019, -2.1458922825255335, -1.5255277792560022, 0.014332280494272709] # End_2
    # end_plate_0 = [1.6935619115829468, -1.0261858862689515, 1.5369141737567347, -2.0552860699095667, -1.5954092184649866, 4.359703063964844] # End_3
    # end_plate_0 =  [1.6784923076629639, -0.9912229341319581, 1.4889605681048792, -2.076402326623434, -1.5669849554644983, 4.669535160064697] # End_4

    def goto(pos):
        robot.move_joint_list(pos, 0.7, 0.5, 0.05)
    def open_gripper():
        gripper.move(0, 125, 125)  # Open Gripper

    def close_gripper():
        gripper.move(200, 125, 125)  # Close Gripper

 
    goto(new_home)
    open_gripper()

    goto(vial_pickup_1)
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
    goto(end_plate_intermediate_1)
    goto(end_plate_1)
    open_gripper()
    goto(new_home)

def degreestorad(list):
    for i in range(6):
        list[i] = list[i] * (math.pi / 180)
    return list

if __name__ == '__main__':
    asyncio.run(main())