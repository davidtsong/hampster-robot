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
    S_t = 20 # wheel speed
    T_r = 30  # turning radius - smaller will track close to curve, but oscillate
    b2 = 20  # half distance between two wheels in mm
    Kp = .011
    d = deque(maxlen=15)
    robot = gRobotList[0]
    error = 0
    done = False
    print "start drive forward"
    while len(d) < 100 and done == False:
        floor_l = robot.get_floor(0)
        floor_r = robot.get_floor(1)
        sensor_diff = floor_l - floor_r

        if(abs(sensor_diff) <=1 and floor_l <= 70):
            d.append(sensor_diff)

        if(floor_l < 20 and floor_r < 20):
            done = True
        error = error - error / 4 + sensor_diff

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
    print "found line"
    time.sleep(.55)
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
    # pathraw = ['0-3', '1-3', '2-3', '2-2', '3-2', '4-2', '4-1']
    pathraw = ['0-3','1-3','2-3','2-2','3-2', '4-2', '4-1']
    path = []
    commands = []
    i = 0
    direction = None
    #up = 1 right = 2 down = 3 left = 4 | All relative to the robot itself
    while not gQuit:

        if (gState == "P"):
            for i in range(len(pathraw)):
                pathraw[i].split("-")
                path.append([int(pathraw[i][0]),int(pathraw[i][2])])  
            print path      
            #now in format [[0,3][1,3]]
            for i in range(len(path)):
                #0 index = x and 1 index = y Lowest is biggest
                if not i+1 == len(path):
                    nextCoord = path[i+1]
                    currentCoord = path[i]

                    #needs to compensate for the current orientation
                    if(currentCoord[0] == nextCoord[0]-1):#go right
                        print "go rite"
                        if(direction == None):#first run through; set initial direction
                            direction = "Right"
                            print "set to right"
                        if(direction == "Up"):
                            turnRight()
                            time.sleep(1)
                            driveForward()
                            time.sleep(1)
                        if(direction == "Right"):
                            driveForward()
                            time.sleep(1)
                        if(direction == "Down"):
                            turnLeft()
                            time.sleep(1)
                            driveForward()
                            time.sleep(1)
                        if(direction == "Left"):
                            turnRight()
                            time.sleep(1)
                            turnRight()
                            time.sleep(1)
                            driveForward(0)
                            time.sleep(1)
                        direction = "Right"

                    elif(currentCoord[0] == nextCoord[0]+1):#go left
                        print "go left"
                        if(direction == None):#first run through; set initial direction
                            direction = "Left"
                            print "set to left"
                        if(direction == "Up"):
                            turnLeft()
                            time.sleep(1)
                            driveForward()
                            time.sleep(1)
                        if(direction == "Right"):
                            turnRight()
                            time.sleep(1)
                            turnRight()
                            time.sleep(1)
                            driveForward()
                            time.sleep(1)
                        if(direction == "Down"):
                            turnRight()
                            time.sleep(1)
                            driveForward()
                            time.sleep(1)
                        if(direction == "Left"):
                            driveForward()
                            time.sleep(1)
                        direction = "Left"
                    elif(currentCoord[1] == nextCoord[1]-1):#go down
                        print "go down"
                        if(direction == None):#first run through; set initial direction
                            direction = "Down"
                            print "set to down"
                        if(direction == "Up"):
                            turnRight()
                            time.sleep(1)
                            turnRight()
                            time.sleep(1)
                            driveForward(0)  
                            time.sleep(1)                                              
                        if(direction == "Right"):
                            turnRight()
                            time.sleep(1)
                            driveForward()
                            time.sleep(1)
                        if(direction == "Down"):
                            driveForward()
                            time.sleep(1)
                        if(direction == "Left"):
                            turnLeft()
                            time.sleep(1)
                            driveForward()
                            time.sleep(1)
                        direction = "Down"
                    elif(currentCoord[1] == nextCoord[1]+1):#go up
                        print "go up"
                        if(direction == None):#first run through; set initial direction
                            direction = "Up"
                            print "set to up"
                        if(direction == "Up"):
                            driveForward() 
                            time.sleep(1)                                                                     
                        if(direction == "Right"):
                            turnLeft()
                            time.sleep(1)
                            driveForward()
                            time.sleep(1)
                        if(direction =="Down"):
                            turnRight()
                            time.sleep(1)
                            turnRight()
                            time.sleep(1)
                            driveForward(0) 
                            time.sleep(1) 
                        if(direction == "Left"):
                            turnRight()
                            time.sleep(1)
                            driveForward()
                            time.sleep(1)
                        direction = "Up"
                #find out what direction to turn

                # x = path[i+1]
            # driveForward()
            # floor_l = robot.get_floor(0)
            # floor_r = robot.get_floor(1)
            # sensor_diff = floor_l - floor_r

            # print "diff:", sensor_diff, "D: ", sensor_diff, "L: ",floor_l, "R: ", floor_r,  "T_r:", T_r, "D: ", len(d)
        
            gState = ""
            print "done driving path"
            path = []

        time.sleep(0.01)
    print gState
    print "stop the robot"
                


def behavior_pi_controller():
    global gState
    turning = False
    robot = gRobotList[0]

    while not gQuit:

        if (gState == "PI"):
            print "Battery is at " ,gRobotList[0].get_battery()
            driveForward()
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
