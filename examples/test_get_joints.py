import sys
import os
import time
import argparse
import math 
# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))

from utils.UR_Functions import URfunctions as URControl

HOST = "192.168.0.2"
PORT = 30003

def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    print(robot.get_current_joint_positions().tolist())
    #print(robot.get_current_tcp())
if __name__ == '__main__':
     main()


# Position A: Above Vial Start - [1.0500986576080322, -1.2801984411529084, 1.8859952131854456, -2.209724565545553, -1.5605104605304163, 1.2218868732452393]
# Pos A-2: In the Vial - [1.0490845441818237, -1.2347015899470826, 1.8862054983722132, -2.2256490192809046, -1.5525544325457972, 1.0632829666137695]
# Position C: Above Vial End - [1.5515978336334229, -1.6546455822386683, 2.3073864618884485, -2.1558286152281703, -1.560286823903219, 1.2228846549987793]