
import Tkinter as tk
import threading
from HamsterAPI.comm_usb import RobotComm
from gridapi import *

gRobotList = None
gRobotNum = 2
rawPath = []
commands = []
robot = None
obs = []
MyGraph = None
endNode = "0-4"
startNode = "0-0"
destCoor = [0,0] # 0 = current 1 = dest
foundObs = False
#todo move these to api class and find a way to get a reference to robot instance
def forward():
    S_t = 20 # wheel speed
    T_r = 30  # turning radius - smaller will track close to curve, but oscillate
    b2 = 20  # half distance between two wheels in mm
    Kp = .0125
    error = 0
    done = False
    sensor_diff = 0
    print "start drive forward"
    
    while done == False:
        floor_l = robot.get_floor(0)
        floor_r = robot.get_floor(1)
        sensor_diff = floor_l - floor_r + .0001

        if(floor_l < 20 and floor_r < 20):
            done = True
        T_r = int(round(190 / abs(Kp * sensor_diff + .01)))    
        if (sensor_diff < 60):  # steer left
            s_l = S_t * (T_r - b2) / (T_r + b2)
            s_r = S_t
        elif (sensor_diff > 60):
            s_r = S_t * (T_r - b2) / (T_r + b2)
            s_l = S_t
        else:
            s_l = s_r = S_t
        print "diff:", sensor_diff, "D: ", sensor_diff, "L: ",floor_l, "R: ", floor_r,  "T_r:", T_r
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

def checkObs():
    global obs
    global foundObs
    global rawPath
    global commands
    if robot.get_proximity(1) > 60 and robot.get_proximity(0) > 60:
        print "Found an obstacle"
        foundObs = True
        obs.append(destCoor[1])
        rawPath = []
        print "obs coor : ", destCoor[1]
        MyGraph = None
        MyGraph = Graph(canvas)
        MyGraph.columns = 7
        MyGraph.rows = 5
        createGraphView(MyGraph,obs,str(destCoor[0][0])+"-"+str(destCoor[0][1]),endNode)
        rawPath = MyGraph.BFS()
        print "Initial Path : ", rawPath
        commands = buildCommandQueue(rawPath, robot,1)
    else: 
        print "No obstacle!"
    
def runCommands():
    global obs
    global robot
    global destCoor
    global foundObs
    robot = gRobotList[0]
    done = False
    rawPath = MyGraph.BFS()
    print "Initial Path : ", rawPath
    commands = buildCommandQueue(rawPath, robot,1)

    while not done:
        
        for i in range(len(commands)):
            if not foundObs:
                currentCommand = commands[i][0] 
                print currentCommand + " Started"
                if currentCommand == "checkObs":
                    destCoor[0] = commands[i][1]
                    destCoor[1] = commands[i][2]
                    eval(currentCommand+"()")
                elif currentCommand == "end":
                    done = True
                    print "We DONEEE"
                else:
                    eval(currentCommand+"()")
                print currentCommand + " Ended"
                time.sleep(1)
    print " DONE WITH RUN COMMANDS"



def start(event=None):
    global commands
    commandThread = threading.Thread(target=runCommands)
    commandThread.daemon = True
    commandThread.start()

    

    
        # try:
        #     eval(commands[i][0] + "()")
        #     if robot.get_proximity(1) > 60 and robot.get_proximity(2) > 60:
        #         print "Found an obs!"
        #         commands = []
        #         obs.append(commands[i][4])
        #         resetGrid(commands[i][3])
        #     time.sleep(1)
        # except IndexError:
        #     pass
        # continue
        
        

def exitProg(event=None):
    frame.quit()

def main(argv=None):
    global gRobotNum
    global frame
    global gQuit
    global gState
    global rawPath
    global gRobotList
    global MyGraph
    global end
    global canvas

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
    MyGraph.columns = 7
    MyGraph.rows = 5
    createGraphView(MyGraph,obs,startNode,endNode)
    
    
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