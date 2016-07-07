'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys, os #, getopt
import time  # sleep
import signal
import threading
import Tkinter as tk
#from HamsterAPI.comm_ble import RobotComm
from HamsterAPI.comm_usb import RobotComm
# from Behavior import motion, color

# if (sys.platform == 'darwin'):
#     from PyObjCTools import AppHelper

gMaxRobotNum = 8; # max number of robots to control
gRobotList = None
gBehavior1 = None
gBehavior2 = None
      
'''
def behavior_square():
    global gRobotList
 
    while not gQuit:
        if (len(gRobotList) > 0):
          for robot in gRobotList:
            for i in range(0,3):
                time.sleep(1)
                robot.set_wheel(0, 30)
                robot.set_wheel(1, 30)
                time.sleep(2)
                robot.set_wheel(0, -25)
                robot.set_wheel(1, 25)
                #time.sleep(1)

        time.sleep(0.01)
    print "robot stops moving"
'''

#house keeping
def clean_up():
    global gBehavior1, gBehavior2

    print "cleaning up..."
    gBehavior1.set_bQuit(True)
    gBehavior2.set_bQuit(True)
    time.sleep(1)
    if (sys.platform == 'darwin'):
       AppHelper.stopEventLoop()

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    clean_up()

signal.signal(signal.SIGINT, signal_handler)


def main(argv=None):
    # instantiate COMM object
    global gMaxRobotNum
    global gBehavior1, gBehavior2

    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'

    r=tk.Tk()
    
    # instanciate Robot
    global gRobotList
    gRobotList = comm.robotList

    # start a behavior tread
    # gBehavior1 = motion.Behavior("motion", gRobotList)
    # behavior_thread1 = threading.Thread(target=gBehavior1.behavior_loop)
    # behavior_thread1.daemon = True
    # behavior_thread1.start()

    # gBehavior2 = color.Behavior("color", gRobotList)
    # behavior_thread2 = threading.Thread(target=gBehavior2.behavior_loop)
    # behavior_thread2.daemon = True
    # behavior_thread2.start()

    #cleaning up when terminated
    if (sys.platform == 'win32' or os.name == 'nt'):
        os.system("pause")
        pass
    elif os.name == 'posix':
        if (sys.platform == 'darwin'):
            print "runConsoleEventLoop"
            # AppHelper.runConsoleEventLoop()
        else:
            while True:
                time.sleep(0.1)
    else:
        print "Error: Unknown OS"

    # behavior_thread1.join()
    # behavior_thread2.join()
    
    r.mainloop()
    for robot in gRobotList:
        robot.reset()
    time.sleep(1.0)
    comm.stop()
    comm.join()

    print("terminated!")

if __name__ == "__main__":
    sys.exit(main())