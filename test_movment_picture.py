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

def capture_image():
    save_path = os.path.join(current_dir, 'test_picture_store')
    os.makedirs(save_path, exist_ok=True)
    
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return
    
    ret, frame = cam.read()
    if ret:
        img_name = os.path.join(save_path, "captured_image.jpg")
        cv2.imwrite(img_name, frame)
        print(f"Image saved at {img_name}")
    else:
        print("Failed to capture image.")
    
    cam.release()
    cv2.destroyAllWindows()

async def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    gripper = RobotiqGripper()
    gripper.connect("192.168.0.2", 63352)

    new_home = [1.3348536491394043, -1.6144734821715296, 1.5730488936053675, -1.5615404548919578, -1.5539191404925745, -0.2927349249469202]
    vial_pickup_2 = [1.0893298387527466, -1.1207396549037476, 1.7084930578814905, -2.1476899586119593, -1.5345671812640589, 1.062324047088623]
    vial_plate_intermediate = [1.1170587539672852, -1.4987735611251374, 1.561568562184469, -1.6459490261473597, -1.552575413380758, 1.0632418394088745]
    stirrer_position = [1.353271722793579, -1.4905654725483437, 1.9034879843341272, -1.9808117351927699, -1.5576022307025355, -0.2884419600116175]
    camera_position = [1.5405631065368652, -1.9327041111388148, 2.2914238611804407, -1.9269162617125453, -1.5510247389422815, -0.29272157350649053]
    end_plate_2 = [1.683842420578003, -1.0204988282969971, 1.533896271382467, -2.0565110645689906, -1.569904629384176, -0.2896679083453577]

    def goto(pos):
        robot.move_joint_list(pos, 0.7, 0.5, 0.05)
    
    def open_gripper():
        gripper.move(0, 125, 125)
    
    def close_gripper():
        gripper.move(200, 125, 125)

    goto(new_home)
    open_gripper()
    goto(vial_pickup_2)
    close_gripper()
    goto(vial_plate_intermediate)
    goto(new_home)
    goto(stirrer_position)
    open_gripper()
    goto(new_home)
    await asyncio.sleep(5)
    goto(stirrer_position)
    close_gripper()
    goto(new_home)
    goto(camera_position)
    
    # Capture image after moving to camera position
    capture_image()
    
    await asyncio.sleep(5)
    goto(new_home)
    goto(end_plate_2)
    open_gripper()
    goto(new_home)

def degreestorad(list):
    for i in range(6):
        list[i] = list[i] * (math.pi / 180)
    return list

if __name__ == '__main__':
    asyncio.run(main())





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
#         if k % 256 == 27:
#             # ESC pressed
#             print("Escape hit, closing...")
#             break

#         elif k % 256 == 32:
#             # SPACE pressed
#             img_name = "opencv_frame_{}.png".format(img_counter)
#             cv2.imwrite(img_name, frame)
#             print("{} written!".format(img_name))
#             img_counter += 1
#     cam.release()
#     cv2.destroyAllWindows()
# camera_thread = threading.Thread(target=asyncio.run, args=(open_camera(),))
# camera_thread.start()