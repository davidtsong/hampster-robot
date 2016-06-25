

import time  # sleep

import threading

from HamsterAPI.comm_usb import RobotComm

import Tkinter as tk

import Queue

from simple_FSM_Q import *



gMaxRobotNum = 1; # max number of robots to control

gRobotList = None



q = Queue.Queue() #for avoidance



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

  

    State_F.add_transition("b_pressed", "moving_backward", moving_backward)

    State_B.add_transition("f_pressed", "moving_forward", moving_forward)   



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



def f_pressed(event=None):

  print "f pressed"

  e = Event("f_pressed",0)

  q.put(e) 



def b_pressed(event=None):

  print "b pressed"

  e = Event("b_pressed",0)

  q.put(e) 



def main(argv=None):

    # instantiate COMM object

    global gMaxRobotNum



    global q

    q = Queue.Queue()



    comm = RobotComm(gMaxRobotNum)

    comm.start()

    print 'Bluetooth starts'

    

    # instanciate Robot

    global gRobotList

    gRobotList = comm.robotList



    global gQuit 

    gQuit = False



    global frame



    behavior_thread = threading.Thread(target=behavior_simple)

    behavior_thread.daemon = True
    behavior_thread.start()





    frame = tk.Tk()

    canvas = tk.Canvas(frame, bg="white", width=300, height=300)

    canvas.pack(expand=1, fill='both')

    canvas.create_rectangle(175, 175, 125, 125, fill="blue")

 

    button1 = tk.Button(frame,text="Start")

    button1.pack()

    button1.bind('<Button-1>', startRobot)

 

    button2 = tk.Button(frame,text="Exit")

    button2.pack()

    button2.bind('<Button-1>', stopProg)



    canvas.bind_all('<f>', f_pressed)  

    canvas.bind_all('<b>', b_pressed)  



    frame.mainloop()



    print "Cleaning up"

    gQuit = True

    behavior_thread.join()



    for robot in gRobotList:

        robot.reset()

    time.sleep(1.0)

    comm.stop()

    comm.join()



    print("terminated!")



if __name__ == "__main__":

    main()

