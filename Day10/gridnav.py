
import Tkinter as tk
import threading
from HamsterAPI.comm_usb import RobotComm
from gridapi import *

gRobotList = None
gRobotNum = 1
rawPath = []
commands = []
robot = None
#todo move these to api class and find a way to get a reference to robot instance
def forward():
    S_t = 20 # wheel speed
    T_r = 30  # turning radius - smaller will track close to curve, but oscillate
    b2 = 20  # half distance between two wheels in mm
    Kp = .011
    error = 0
    done = False
    print "start drive forward"
    
    while done == False:
        floor_l = robot.get_floor(0)
        floor_r = robot.get_floor(1)
        sensor_diff = floor_l - floor_r

        if(floor_l < 20 and floor_r < 20):
            done = True
        T_r = int(round(190 / abs(Kp * error + .01)))    
        if (sensor_diff < 60):  # steer left
            s_l = S_t * (T_r - b2) / (T_r + b2)
            s_r = S_t
        elif (sensor_diff > 60):
            s_r = S_t * (T_r - b2) / (T_r + b2)
            s_l = S_t
        else:
            s_l = s_r = S_t
       # print "diff:", sensor_diff, "D: ", sensor_diff, "L: ",floor_l, "R: ", floor_r,  "T_r:", T_r, "D: ", len(d)
        # print "floor l, r", floor_l, floor_r, sensor_diff

        robot.set_wheel(0, s_l)
        robot.set_wheel(1, s_r)
        time.sleep(.01)
    print "found line"
    time.sleep(.55)
    robot.set_wheel(0,0)
    robot.set_wheel(1,0)

def right():
    robot = gRobotList[0]
    robot.set_wheel(0, 50)
    robot.set_wheel(1, -50)
    time.sleep(.485)
    robot.set_wheel(0, 0)
    robot.set_wheel(1, 0)


def left():
    robot = gRobotList[0]
    robot.set_wheel(0, -50)
    robot.set_wheel(1, 50)
    time.sleep(.485)
    robot.set_wheel(0, 0)
    robot.set_wheel(1, 0)

def start(event=None):
    global commands
    global robot
    robot = gRobotList[0]
    commands = buildCommandQueue(rawPath, robot)
    for i in range(len(commands)):
        # if robot.get_proximity[0] > 75 and robot.get_proximity[1] > 75
        #     #see what direction to remove node from

        #     rawPath = MyGraph.BFS()
        #     commands = buildCommandQueue(rawPath,robot)
        #     i = 0
        eval(commands[i])

def exitProg(event=None):
    frame.quit()
def main(argv=None):
    global gRobotNum
    global frame
    global gQuit
    global gState
    global rawPath
    global gRobotList

    obs = []
    commands = []
    comm = RobotComm(gRobotNum)
    comm.start()
    print "Comm Starts"
    gRobotList = comm.robotList
    gQuit = False
    gState = False

    frame = tk.Tk()
    canvas = tk.Canvas(frame, bg="white", width=500, height=500)
    canvas.pack(expand=1, fill='both')
    button_start = tk.Button(frame, text="Start")
    button_start.pack(side="bottom")
    button_start.bind('<Button-1>', start)

    button_stop = tk.Button(frame, text="Stop")
    button_stop.pack(side="bottom")
    button_stop.bind('<Button-1>', exitProg)
    # behavior_start = threading.Thread(target="behavior_drive")
    # behavior_start.daemon = True
    # behavior_start.start()

    
    MyGraph = Graph(canvas)
    
    draw_nodes(MyGraph, 5, 4)
    MyGraph.set_start("0-0")
    MyGraph.set_goal("3-4")
    
    closeNode(MyGraph,"2-0")
    closeNode(MyGraph,"1-2")
    closeNode(MyGraph,"3-1")
    closeNode(MyGraph,"3-3")

    #build initial Path
    rawPath = MyGraph.BFS()
    
    frame.mainloop()

    gQuit = True
    print "Quitting"
    for robot in gRobotList:
        robot.reset()
    time.sleep(1.0)
    comm.stop()
    comm.join()


if __name__ == "__main__":
    main()