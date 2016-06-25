'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Written By Dr. David Zhu

   Last updated: May 28th, 2016

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import time  # sleep
import Tkinter as tk
import threading
#from HamsterAPI.comm_ble import RobotComm
from HamsterAPI.comm_usb import RobotComm

gMaxRobotNum = 1; # max number of robots to control
gRobotList = None
Finished = None

def driveStraight(robot,duration,speed):
        robot.set_wheel(0,speed)
        robot.set_wheel(1,speed)
        time.sleep(duration)
        robot.set_wheel(0,0)
        robot.set_wheel(1,0)

def turnRight(robot):
        robot.set_wheel(0,50)
        robot.set_wheel(1,-50)
        time.sleep(.453)
        robot.set_wheel(0,0)
        robot.set_wheel(1,0)

def turnLeft(robot):
        robot.set_wheel(0,-50)
        robot.set_wheel(1,50)
        time.sleep(.453)
        robot.set_wheel(0,0)
        robot.set_wheel(1,0)

def setSpeed(speedLeft, speedRight):
    if len(gRobotList) > 0:
        for robot in gRobotList:
            robot.set_wheel(0,speedLeft);
            robot.set_wheel(1,speedRight);
    

def behavior_square():
    global Finished
    while not gQuit:
        # put code here
        if Behavior == "Square" and Finished == False:
            if(len(gRobotList) > 0):
                for robot in gRobotList:
                    turnLeft(robot)
                    # for i in range(4):
                    #     driveStraight(robot,1,100)
                    #     turnRight(robot)    
                    Finished = True
            time.sleep(0.01)
        time.sleep(0.01)
        
    print "robot stops moving"

def behavior_shy():

    while not gQuit:
        if Behavior == "Shy":
            if (len(gRobotList) > 0):    
                print "k"
            time.sleep(0.1)                   
        time.sleep(0.01)
    print "robot stops shy"
        
def behavior_follow():
    print "put robot follow behavior code"
    while not gQuit:

        time.sleep(0.01)
    print "robot stops follow"
        
def behavior_dance():
    print "put robot dance code here - or any other interesting robot behavior"
    while not gQuit:
        # put code here
        time.sleep(0.01)
    print "robot stops dance"

def Square(event=None):
    global Behavior
    global Finished
    Behavior = "Square"
    Finished = False

def Shy(event=None):
    global Behavior
    Behavior = "Shy"

def Follow(event=None):
    global Behavior
    Behavior = "Follow"

def Dance(event=None):
    global Behavior
    Behavior = "Dance"

def Pause(event=None):
    global Behavior
    Behavior = False
    if (len(gRobotList) > 0):
        for robot in gRobotList:
            robot.set_wheel(0,0)
            robot.set_wheel(1,0)
            robot.set_musical_note(0)       

def stopProg(event=None):
    frame.quit()
    print "Exit"

def main(argv=None):
    # instantiate COMM object
    global gMaxRobotNum
    global frame
    global behavior_thread1, behavior_thread2
    global gRobotList
    global gQuit
    global Behavior

    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'
    
    gRobotList = comm.robotList
    #gRobotArray = comm.robotArray

    gQuit = False
    Behavior = False


    behavior_thread0 = threading.Thread(target=behavior_square)
    behavior_thread0.daemon = True
    behavior_thread0.start()

    behavior_thread1 = threading.Thread(target=behavior_shy)
    behavior_thread1.daemon = True
    behavior_thread1.start()

    behavior_thread2 = threading.Thread(target=behavior_follow)
    behavior_thread2.daemon = True
    behavior_thread2.start()

    behavior_thread3 = threading.Thread(target=behavior_dance)
    behavior_thread3.daemon = True
    behavior_thread3.start()

    frame = tk.Tk()
    canvas = tk.Canvas(frame, bg="white", width=300, height=300)
    canvas.pack(expand=1, fill='both')
    canvas.create_rectangle(175, 175, 125, 125, fill="green")
    
    # lightL = rectangle()

    button0 = tk.Button(frame,text="Square")
    button0.pack(side='left')
    button0.bind('<Button-1>', Square)

    button1 = tk.Button(frame,text="Shy")
    button1.pack(side='left')
    button1.bind('<Button-1>', Shy)

    button2 = tk.Button(frame,text="Follow")
    button2.pack(side='left')
    button2.bind('<Button-1>', Follow)

    button3 = tk.Button(frame,text="Dance")
    button3.pack(side='left')
    button3.bind('<Button-1>', Dance)

    button4 = tk.Button(frame,text="Pause")
    button4.pack(side='left')
    button4.bind('<Button-1>', Pause)

    button5 = tk.Button(frame,text="Exit")
    button5.pack(side='left')
    button5.bind('<Button-1>', stopProg)

    #Button Bindings
   


    frame.mainloop()
    
    print "Cleaning up"
    gQuit = True
    if behavior_thread1:
        behavior_thread1.join()
    if behavior_thread2:
        behavior_thread2.join()

    for robot in gRobotList:
      robot.reset()
    time.sleep(1.0)
    comm.stop()
    comm.join()

    print("terminated!")


if __name__ == "__main__":
    #sys.exit(main())
    main()