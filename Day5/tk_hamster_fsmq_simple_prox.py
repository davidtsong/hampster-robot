'''

/* =======================================================================

   (c) 2015, Kre8 Technology, Inc.



   Obstacle Avoidance Implemented As FSM (avoid oscillation)



   By:            David Zhu

   Last Updated:  6/10/16



   PROPRIETARY and CONFIDENTIAL

   ========================================================================*/

'''

import time  # sleep

import threading

from HamsterAPI.comm_usb import RobotComm

import Tkinter as tk

from simple_FSM_Q import *

import Queue



gMaxRobotNum = 1; # max number of robots to control

gRobotList = None



q = Queue.Queue() #for avoidance



def monitor_sensors():

  just_turned_on = True



  while not gQuit:

   if len(gRobotList) > 0:



    if (just_turned_on):

      time.sleep(1)

      just_turned_on = False #the first time the robot connect, the sensor data is empty for the first second or so



    robot = gRobotList[0]

    p_l = robot.get_proximity(0)

    p_r = robot.get_proximity(1)



    #obstacle detection

    if (p_l > 40 or p_r > 40):

      e = Event("obs_front",p_l+p_r)

      q.put(e) 

    else:

      e = Event("obs_free", p_l+p_r)

      q.put(e)



    time.sleep(0.1)



def moving_forward (robot):

  robot.set_wheel(0,30)

  robot.set_wheel(1,30)

  return True



def moving_backward (robot):

  robot.set_wheel(0,-30)

  robot.set_wheel(1,-30)

  return True



def behavior_simple():



    Simple_Behavior = StateMachine()

    State_F = Simple_Behavior.add_state("moving_forward")

    State_B = Simple_Behavior.add_state("moving_backward")



    # initializing

    Simple_Behavior.set_start("moving_forward")

    Simple_Behavior.set_current("moving_forward")

  

    State_F.add_transition("obs_front", "moving_backward", moving_backward)

    State_B.add_transition("obs_free", "moving_forward", moving_forward)   



    while not gQuit:

          if len(gRobotList) > 0:

            Simple_Behavior.run(gRobotList[0],q)

          time.sleep(0.01)



def stopProg(event=None):

    gQuit = True

    frame.quit()

    print "Exit"



def startRobot(event=None):

  if (len(gRobotList) > 0):

      print "starting robot"

      for robot in gRobotList:

          robot.set_wheel(0,40)

          robot.set_wheel(1,40)  

  else:

      print "waiting for robot"





def main(argv=None):

    # instantiate COMM object

    global gMaxRobotNum

    comm = RobotComm(gMaxRobotNum)

    comm.start()

    print 'Bluetooth starts'

    

    # instanciate Robot

    global gRobotList

    gRobotList = comm.robotList



    global gQuit 

    gQuit = False



    global q

    q = Queue.Queue()



    global frame



    monitor_thread = threading.Thread(target=monitor_sensors)

    monitor_thread.daemon = True

    monitor_thread.start()



    behavior_thread = threading.Thread(target=behavior_simple)

    behavior_thread.daemon = True

    behavior_thread.start()



    frame = tk.Tk()

    canvas = tk.Canvas(frame, bg="white", width=300, height=300)

    canvas.pack(expand=1, fill='both')

    canvas.create_rectangle(175, 175, 125, 125, fill="green")

 

    button1 = tk.Button(frame,text="Start")

    button1.pack()

    button1.bind('<Button-1>', startRobot)

 

    button2 = tk.Button(frame,text="Exit")

    button2.pack()

    button2.bind('<Button-1>', stopProg)





    frame.mainloop()

    

    print "Cleaning up"

    gQuit = True

    monitor_thread.join()

    behavior_thread.join()



    for robot in gRobotList:

        robot.reset()

    time.sleep(1.0)

    comm.stop()

    comm.join()



    print("terminated!")



if __name__ == "__main__":

    main()

