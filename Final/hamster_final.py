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
#from HamsterAPI.comm_ble import RobotComm
from HamsterAPI.comm_usb import RobotComm
from simple_graph_BFS_path import *

gMaxRobotNum = 2; # max number of robots to control
gRobotList = None

shorten = True

path = []

direc = [-1, 0]

graph_width = 7
graph_height = 5
obs_list = []

start = "6-0"
goal = "6-2"

def behavior_path_controller(data):
    global path
    global direc
    global goal
    global shorten

    canvas = data

    pos = [int(path[0][0]), int(path[0][-1])]

    finished = False

    while not gQuit:
        if (len(gRobotList) > 0):
            if (gState == "PID"):
                robot = gRobotList[0]

                
                if shorten:
                    path = path[1:]

                next_command = []

                if not finished and len(path) == 0:
                    next_command.append('s')
                    finished = True
                    goal_position = [int(goal[0]), int(goal[-1])]
                    if pos != goal_position:
                        wipeMap(canvas, pos)

                elif len(path) > 0:
                    item = path[0]
                    item = [int(item[0]), int(item[-1])]
                    diff = [item[0]-pos[0], item[1]-pos[1]]
                    
                    if not obsCheck(robot, canvas, pos, direc):

                        if direc != diff:
                            
                            shorten = False
    
                            if diff == [1,0]:
                                if direc == [0,1]:
                                    next_command.append('d')
                                if direc == [0,-1]:
                                    next_command.append('a')
                                if direc == [-1,0]:
                                    next_command.append('a')
                                    next_command.append('a')
                
                            if diff == [0,1]:
                                if direc == [1,0]:
                                    next_command.append('a')
                                if direc == [0,-1]:
                                    next_command.append('a')
                                    next_command.append('a')
                                if direc == [-1,0]:
                                    next_command.append('d')
                
                            if diff == [-1,0]:
                                if direc == [1,0]:
                                    next_command.append('a')
                                    next_command.append('a')
                                if direc == [0,-1]:
                                    next_command.append('d')
                                if direc == [0,1]:
                                    next_command.append('a')
                
                            if diff == [0,-1]:
                                if direc == [1,0]:
                                    next_command.append('d')
                                if direc == [-1,0]:
                                    next_command.append('a')
                                if direc == [0,1]:
                                    next_command.append('a')
                                    next_command.append('a')
                        
                        else:
                            next_command.append('w')
                            pos = item
                            shorten = True
    
                        direc = diff
                    
                    

                for item in next_command:

                    print item

                    if item == "w":
                        forward()
                    elif item == "a":
                        turnLeft()
                    elif item == "d":
                        turnRight()
                    elif item == "s":
                        robot.set_wheel(0, 0)
                        robot.set_wheel(1, 0)

                time.sleep(0.1)
        time.sleep(0.01)
    print "stop the robot"

def obsCheck(robot, canvas, pos, direc):
    global gState
    global path
    global obs_list

    prox_l = robot.get_proximity(0)
    prox_r = robot.get_proximity(1)

    view = [pos[0] + direc[0], pos[1] + direc[1]]

    # check for obstacle
    if prox_l > 65 and prox_r > 65 and not view in obs_list:
        gState = ""
        canvas.delete("all")
        addObs(canvas, pos, view)
        return True
    
    return False

def addObs(canvas, pos, view):
    global gState
    global path
    global obs_list
    global goal
    global shorten

    shorten = True
    
    obs_list.append(view)

    NewGraph = Graph(canvas)

    create_grid(NewGraph, graph_width, graph_height, obs_list)

    start = str(pos[0]) + "-" + str(pos[1])

    NewGraph.set_start(start)
    NewGraph.set_goal(goal)

    path = NewGraph.BFS()

    gState = "PID"

def wipeMap(canvas, pos):
    global gState
    
    gState = ""

    canvas.delete("all")


def Path_controller(event=None):
    global gState
    gState = "PID"


def exitProg(event=None):
    frame.quit()
    print "Exit"

def forward(event=None):
    global gState
    gState = ""

    S_t = 20 # wheel speed
    b2 = 20 # half distance between two wheels in mm
    kp = 0.0013

    robot = gRobotList[0]
    time.sleep(1)
    while not gQuit:

        floor_l = robot.get_floor(0)
        floor_r = robot.get_floor(1)
        sensor_diff = floor_l - floor_r

        if floor_l + floor_r < 30:
            robot.set_wheel(0, 20)
            robot.set_wheel(1, 20)
            time.sleep(0.5)
            break

        T_r = 1000

        if sensor_diff != 0:
            T_r = 1/(kp*abs(sensor_diff))

        if (sensor_diff < 0): #steer left
            s_l = int(S_t*(T_r-b2)/(T_r+b2))
            s_r = S_t
        elif (sensor_diff > 0):
            s_r = int(S_t*(T_r-b2)/(T_r+b2))
            s_l = S_t
        else:
            s_l = s_r = S_t

        robot.set_wheel(0,s_l)
        robot.set_wheel(1,s_r)
        time.sleep(0.1)
    gState = "PID"
    

def turnRight(event=None):
    global gState
    gState = ""
    robot = gRobotList[0]
    robot.set_wheel(0,30)
    robot.set_wheel(1,-30)
    time.sleep(.85)
    robot.set_wheel(0, 0)
    robot.set_wheel(1, 0)
    gState = "PID"

def turnLeft(event=None):
    global gState
    gState = ""
    robot = gRobotList[0]
    robot.set_wheel(0,-30)
    robot.set_wheel(1,30)
    time.sleep(.85)
    robot.set_wheel(0, 0)
    robot.set_wheel(1, 0)
    gState = "PID"

def main(argv=None):

    # instantiate COMM object

    global gMaxRobotNum
    global frame
    global gRobotList
    global gQuit
    global gState

    global path
    global start
    global goal

    comm = RobotComm(gMaxRobotNum)
    comm.start()

    print 'Bluetooth starts'

    gRobotList = comm.robotList

    gQuit = False
    gState = False

    frame = tk.Tk()

    canvas = tk.Canvas(frame, bg="white", width=600, height=600)
    canvas.pack(expand=1, fill='both')
    # canvas.create_rectangle(175, 175, 125, 125, fill="green")

    MyGraph = Graph(canvas)

    create_grid(MyGraph, graph_width, graph_height, obs_list)

    MyGraph.set_start(start)
    MyGraph.set_goal(goal)

    path = MyGraph.BFS()


    canvas.bind_all('<x>', Path_controller)

    behavior_thread5 = threading.Thread(target=behavior_path_controller, args=(canvas,))
    behavior_thread5.daemon = True
    behavior_thread5.start()

    button = tk.Button(frame,text="Path")
    button.pack()
    button.bind('<Button-1>', Path_controller)

    button6 = tk.Button(frame,text="Exit")
    button6.pack()
    button6.bind('<Button-1>', exitProg)

    frame.mainloop()
    print "Cleaning up"
    gQuit = True
    for robot in gRobotList:
      robot.reset()
    time.sleep(1.0)
    comm.stop()
    comm.join()
    print("terminated!")

if __name__ == "__main__":
    #sys.exit(main())
    main()