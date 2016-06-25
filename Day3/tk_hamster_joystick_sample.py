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
#for PC, need to import from commm_usb

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

def display_sensors(canvas):
    l_id = None
    # create a rectangle for a robot at the center 
    # create a line segment for drawing the left proximilty sensor
    # create a line segment for drawing the right proxijity sensor
    # creat a rectangle for displaying the left floor sensor 
    # create a rectangle for displaying the right floor sensor

    while not gQuit:
        if (len(gRobotList) > 0):
            mycanvas = canvas
            robot = gRobotList[0]
            # display proximity sensors
            prox_l = robot.get_proximity(0)
            prox_r = robot.get_proximity(1)
            print "proximity sensors", prox_l, prox_r
            # put code here to draw proxity
            if not l_id == None:
                canvas.delete(l_id)
                canvas.delete(r_id)

            lineL = (125,125,125,prox_l*2)
            lineR = (175,125,175,prox_r*2)
            l_id = mycanvas.create_rectangle(lineL, fill="red")
            r_id = mycanvas.create_rectangle(lineR, fill="red")

            # mycanvas.coords(l_id, 125,125,125,10)
            # mycanvas.coords(r_id, 175,175,175,10)

            rect = (125,125,175,175)
            rect_id = mycanvas.create_rectangle(rect,fill="green")


            # display floor sensors
            floor_l = robot.get_floor(0)
            floor_r = robot.get_floor(1)
            print "proximity sensors", prox_l, prox_r
            # put code here to draw floor sensors
            
            if floor_l >= 50:
                colorL = "white"
            if floor_l < 50:
                colorL = "black"
            if floor_r >= 50:
                colorR = "white"
            if floor_r < 50:
                colorR = "black"
            rect_L = (130,130,135,135)
            rect_L_id = mycanvas.create_rectangle(rect_L, fill=colorL)
            rect_R = (165,130,170,135)
            rect_R_id = mycanvas.create_rectangle(rect_R,fill=colorR)


            
        else:
            print "waiting for robot"
        time.sleep(0.1)
    print "quiting"
    m.quit()

def stopProg(event=None):
    global gQuit

    gQuit = True
    print "Exit"

def main():
    global gMaxRobotNum; # max number of robots to control
    global gRobotList
    global gQuit
    global m

    gMaxRobotNum = 1
    # thread to scan and connect to robot
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'

    gRobotList = comm.robotList

    gQuit = False

    m = tk.Tk() #root
    mycanvas = tk.Canvas(m, bg="white", width=300, height= 300)
    mycanvas.pack()

  # start a watcher thread
    sensor_display_thread = threading.Thread(target=display_sensors, args=(mycanvas,))
    sensor_display_thread.daemon = True
    sensor_display_thread.start()

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