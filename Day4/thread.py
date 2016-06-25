'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          Joystick for Hamster
   By:            David Zhu
   Last Updated:  6/10/16

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import threading
import Tkinter as tk  # using Python 3
import time  # sleep
from HamsterAPI.comm_usb import RobotComm
import Queue
#for PC, need to import from commm_usb

turning = False
def turnRight(robot):
    global turning

    turning = True;
    robot.set_wheel(0,50)
    robot.set_wheel(1,-50)
    time.sleep(.05)
    robot.set_wheel(0,0)
    robot.set_wheel(1,0)
    turning = False

def turnLeft(robot):
    global turning

    turning = True;
    robot.set_wheel(0,-50)
    robot.set_wheel(1,50)
    time.sleep(.05)
    robot.set_wheel(0,0)
    robot.set_wheel(1,0)
    turning = False

def move_up(event=None):
    if (len(gRobotList) > 0):
        for robot in gRobotList:
            robot.set_wheel(0,30)
            robot.set_wheel(1,30)
    else:
        print "waiting for robot"

def move_down(event=None):
    if (len(gRobotList) > 0):
        for robot in gRobotList:
          robot.set_wheel(0,-30)
          robot.set_wheel(1,-30)
    else:
        print "waiting for robot"

def move_left(event=None):
    if (len(gRobotList) > 0):
        for robot in gRobotList:
            robot.set_wheel(1,30)
            robot.set_wheel(0,-30)
    else:
        print "waiting for robot"

def move_right(event=None):
    if (len(gRobotList) > 0):
        for robot in gRobotList:
            robot.set_wheel(1,-30)
            robot.set_wheel(0,30)
    else:
        print "waiting for robot"

def stop_move(event=None):
    if (len(gRobotList) > 0):
        for robot in gRobotList:
            robot.set_wheel(0,0)
            robot.set_wheel(1,0)
    else:
        print "waiting for robot"

class Event():
    tag = ""
    data = None
    def __init__(self,tag, data):
        self.tag = tag
        self.data = data

def display_sensors(canvas, displayQueue):
    l_id = None
    # create a rectangle for a robot at the center 
    # create a line segment for drawing the left proximilty sensor
    # create a line segment for drawing the right proxijity sensor
    # creat a rectangle for displaying the left floor sensor 
    # create a rectangle for displaying the right floor sensor

    while not gQuit:
        while not displayQueue.empty():
            mycanvas = canvas
            # print "p: ", prox.data, "l : ", light.data, "  ps: ", proxQueue.qsize()," ls: ", lightQueue.qsize()
            event = displayQueue.get()
           # print "pl: ",event.data[0],"pr: ",event.data[1],"fl: ",event.data[2],"fr: ", event.data[3]
            #print "proximity sensors", prox_l, prox_r
            #put code here to draw proxity

            # if not l_id == None:
            #     canvas.delete(l_id)
            #     canvas.delete(r_id)

            # lineL = (125,125,125,prox.data[0]*2)
            # lineR = (175,125,175,prox.data[1]*2)
            # l_id = mycanvas.create_line(lineL, fill="red")
            # r_id = mycanvas.create_line(lineR, fill="red")

            # # mycanvas.coords(l_id, 125,125,125,10)
            # # mycanvas.coords(r_id, 175,175,175,10)

            # rect = (125,125,175,175)
            # rect_id = mycanvas.create_rectangle(rect,fill="green")

            # if light.data[0] >= 50:
            #     colorL = "white"
            # if light.data[0] < 50:
            #     colorL = "black"
            # if light.data[1] >= 50:
            #     colorR = "white"
            # if light.data[1] < 50:
            #     colorR = "black"
            # rect_L = (130,130,135,135)
            # rect_L_id = mycanvas.create_rectangle(rect_L, fill=colorL)
            # rect_R = (165,130,170,135)
            # rect_R_id = mycanvas.create_rectangle(rect_R,fill=colorR)
            time.sleep(.1)
        time.sleep(.01)
    m.quit()

def stopProg(event=None):
    global gQuit

    gQuit = True
    print "Exit"

def watch(displayQueue, navQueue):
    global isWatching
    robot = gRobotList[0]
    while not gQuit:
        while True:
            prox_l = robot.get_proximity(0)
            prox_r = robot.get_proximity(1)
            floor_l = robot.get_floor(0)
            floor_r = robot.get_floor(1)
           # print prox_l, prox_r, floor_l, floor_r
            
            if floor_l < 20 or floor_r < 20:
                event = Event("stop", [])
                navQueue.put(event)
                print "put stop"
            elif prox_l > 70 or prox_r > 70:
                event = Event("action", [prox_l,prox_r])
                navQueue.put(event)
                print "put action"
            else:
                print "put free"
                event = Event("free",[])
                navQueue.put(event)

            event = Event("update", [prox_l, prox_r, floor_l, floor_r])
            displayQueue.put(event)
            time.sleep(.01)

def navigate(navQueue):
    robot = gRobotList[0]
    global turning
    turning == False
    time.sleep(.1)
    global gQuit

    while not gQuit:
        if not navQueue.empty():
            event = navQueue.get()
            print event.tag
            if event.tag == "free":
                robot.set_wheel(0,30)
                robot.set_wheel(1,30)

            if event.tag == "action":
                if event.data[0] > event.data[1]:
                    turnRight(robot)
                else:
                    turnLeft(robot)

            elif event.tag == "stop":
                robot.set_wheel(0,0)
                robot.set_wheel(1,0)
                print "Done"
                gQuit =True
            
            time.sleep(.01)
        #print "nav empty"
    time.sleep(.01)

            
def main():
    global gMaxRobotNum; # max number of robots to control
    global gRobotList
    global gQuit
    global m
    global turning

    gMaxRobotNum = 1
    # thread to scan and connect to robot
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'

    gRobotList = comm.robotList
    displayQueue = Queue.Queue(maxsize=20)
    navQueue = Queue.Queue(maxsize=20)

    gQuit = False

    m = tk.Tk() #root
    mycanvas = tk.Canvas(m, bg="white", width=300, height= 300)
    mycanvas.pack()

    #Start a watcher thread
    watcher = threading.Thread(target=watch, args=(displayQueue,navQueue))
    watcher.daemon = True
    watcher.start()

  # start a display thread
    sensor_display_thread = threading.Thread(target=display_sensors, args=(mycanvas,displayQueue))
    sensor_display_thread.daemon = True
    sensor_display_thread.start()

    navigator = threading.Thread(target=navigate, args=(navQueue,))
    navigator.daemon = True
    navigator.start()
    

    # put code here to bind "wasd" and "x" to the robot motion function defined above 
    # bind "w" to move_up()....
    mycanvas.bind_all('<w>',move_up)
    mycanvas.bind_all('<KeyRelease-w>',stop_move)
    mycanvas.bind_all('<a>', move_left)
    mycanvas.bind_all('<KeyRelease-a>', stop_move)
    mycanvas.bind_all('<s>',move_down)
    mycanvas.bind_all('<KeyRelease-s>',stop_move)
    mycanvas.bind_all('<d>',move_right)
    mycanvas.bind_all('<KeyRelease-d>',stop_move)

    button = tk.Button(m,text="Exit")
    button.pack()
    button.bind('<Button-1>', stopProg)

    m.mainloop()

    for robot in gRobotList:
        robot.reset()

    comm.stop()
    comm.join()
    sensor_display_thread.join()


if __name__== "__main__":
    main()