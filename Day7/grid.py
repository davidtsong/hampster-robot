'''

/* =======================================================================

   (c) 2015, Kre8 Technology, Inc.



   By David J. Zhu

   Last updated: 6/6/16



   PROPRIETARY and CONFIDENTIAL

   ========================================================================*/

'''

import time  # sleep

import Tkinter as tk

import threading

# from HamsterAPI.comm_ble import RobotComm

from HamsterAPI.comm_usb import RobotComm
from datetime import datetime
from collections import deque

gMaxRobotNum = 1  # max number of robots to control
gRobotList = None



def driveForward():
    S_t = 25 # wheel speed
    T_r = 30  # turning radius - smaller will track close to curve, but oscillate
    b2 = 20  # half distance between two wheels in mm
    Kp = .02
    d = deque(maxlen=15)
    robot = gRobotList[0]
    error = 0
    while len(d) < 15:
        floor_l = robot.get_floor(0)
        floor_r = robot.get_floor(1)
        sensor_diff = floor_l - floor_r

        if(abs(sensor_diff) <=1):
            d.append(sensor_diff)
            

        error = error - error / 2 + sensor_diff

        T_r = int(round(190 / abs(Kp * error + .01)))    
                    # T_r = int(abs(Kp * sensor_diff))
        if (sensor_diff < 60):  # steer left
            s_l = S_t * (T_r - b2) / (T_r + b2)
            s_r = S_t
        elif (sensor_diff > 60):
            s_r = S_t * (T_r - b2) / (T_r + b2)
            s_l = S_t
        else:
            s_l = s_r = S_t
        
        print "diff:", sensor_diff, "D: ", sensor_diff, "L: ",floor_l, "R: ", floor_r,  "T_r:", T_r, "D: ", len(d)
        # print "floor l, r", floor_l, floor_r, sensor_diff

        robot.set_wheel(0, s_l)
        robot.set_wheel(1, s_r)
        time.sleep(.01)
    time.sleep(.6)
    robot.set_wheel(0,0)
    robot.set_wheel(1,0)
    d.clear()

def turnRight():
    robot = gRobotList[0]
    robot.set_wheel(0, 50)
    robot.set_wheel(1, -50)
    time.sleep(.485)
    robot.set_wheel(0, 0)
    robot.set_wheel(1, 0)


def turnLeft():
    robot = gRobotList[0]
    robot.set_wheel(0, -50)
    robot.set_wheel(1, 50)
    time.sleep(.485)
    robot.set_wheel(0, 0)
    robot.set_wheel(1, 0)

def behavior_p_controller():
    global gState
    turning = False
    robot = gRobotList[0]
    path = []
    while not gQuit:

        if (gState == "P"):
            

            for command in path:
                print command
            # driveForward()
            # floor_l = robot.get_floor(0)
            # floor_r = robot.get_floor(1)
            # sensor_diff = floor_l - floor_r

            # print "diff:", sensor_diff, "D: ", sensor_diff, "L: ",floor_l, "R: ", floor_r,  "T_r:", T_r, "D: ", len(d)
        
            gState = ""
            print "done driving straight"

        time.sleep(0.01)
    print gState
    print "stop the robot"
                


def behavior_pi_controller():
    global gState
    turning = False
    robot = gRobotList[0]

    while not gQuit:

        if (gState == "PI"):
            
            turnRight()
            # floor_l = robot.get_floor(0)
            # floor_r = robot.get_floor(1)
            # sensor_diff = floor_l - floor_r

            # print "diff:", sensor_diff, "D: ", sensor_diff, "L: ",floor_l, "R: ", floor_r,  "T_r:", T_r, "D: ", len(d)
        
            gState = ""
            print "done turning"

        time.sleep(0.01)
    print gState
    print "stop the robot"

def behavior_pid_controller():
    global gQuit
    global gState
    error = []
    
    while not gQuit:

        if (gState == "PID"):
            
            turnLeft()
            # floor_l = robot.get_floor(0)
            # floor_r = robot.get_floor(1)
            # sensor_diff = floor_l - floor_r

            # print "diff:", sensor_diff, "D: ", sensor_diff, "L: ",floor_l, "R: ", floor_r,  "T_r:", T_r, "D: ", len(d)
        
            gState = ""
            print "done turning"

        time.sleep(0.01)
    print gState
    print "stop the robot"

def P_controller(event=None):

    global gState

    gState = "P"


def PI_controller(event=None):

    global gState

    gState = "PI"


def PID_controller(event=None):

    global gState

    gState = "PID"


def exitProg(event=None):

    frame.quit()

    print "Exit"


def main(argv=None):

    # instantiate COMM object

    global gMaxRobotNum

    global frame

    global gRobotList

    global gQuit

    global gState

    comm = RobotComm(gMaxRobotNum)

    comm.start()

    print 'Bluetooth starts'

    gRobotList = comm.robotList

    gQuit = False

    gState = False

    frame = tk.Tk()

    canvas = tk.Canvas(frame, bg="white", width=300, height=300)

    canvas.pack(expand=1, fill='both')

    canvas.create_rectangle(175, 175, 125, 125, fill="green")

    behavior_thread3 = threading.Thread(target=behavior_p_controller)

    behavior_thread3.daemon = True

    behavior_thread3.start()

    behavior_thread4 = threading.Thread(target=behavior_pi_controller)

    behavior_thread4.daemon = True

    behavior_thread4.start()

    behavior_thread5 = threading.Thread(target=behavior_pid_controller)

    behavior_thread5.daemon = True

    behavior_thread5.start()

    button3 = tk.Button(frame, text="P")

    button3.pack(side='left')

    button3.bind('<Button-1>', P_controller)

    button4 = tk.Button(frame, text="PI")

    button4.pack(side='left')

    button4.bind('<Button-1>', PI_controller)

    button5 = tk.Button(frame, text="PID")

    button5.pack(side='left')

    button5.bind('<Button-1>', PID_controller)

    button6 = tk.Button(frame, text="Exit")

    button6.pack(side='left')

    button6.bind('<Button-1>', exitProg)

    frame.mainloop()

    print "Cleaning up"

    gQuit = True

    if behavior_thread1:
        behavior_thread1.join()

    if behavior_thread2:

        behavior_thread2.join()

    if behavior_thread3:

        behavior_thread3.join()

    for robot in gRobotList:

        robot.reset()

    time.sleep(1.0)

    comm.stop()

    comm.join()

    print("terminated!")


if __name__ == "__main__":

    # sys.exit(main())

    main()
