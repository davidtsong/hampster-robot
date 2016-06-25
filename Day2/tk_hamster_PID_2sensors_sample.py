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
from datetime import datetime


gMaxRobotNum = 1; # max number of robots to control

gRobotList = None



def behavior_2steps(): #using the right floor sensor to follow the left edge of a black line

    S_t = 30 # wheel speed

    T_r = 30 # turning radius - smaller will track close to curve, but oscillate 

    b2 = 20 # half distance between two wheels in mm



    while not gQuit:

        if (gState == "2steps"):

           if (len(gRobotList) > 0):

                robot = gRobotList[0]

                floor_l = robot.get_floor(0)

                floor_r = robot.get_floor(1)

                sensor_diff = floor_l - floor_r

                print "floor l, r", floor_l, floor_r, sensor_diff

                if (sensor_diff < 0): #steer left

                    s_l = S_t*(T_r-b2)/(T_r+b2)

                    s_r = S_t

                elif (sensor_diff > 0):

                    s_r = S_t*(T_r-b2)/(T_r+b2)

                    s_l = S_t

                else:

                    s_l = s_r = S_t

                robot.set_wheel(0,s_l)

                robot.set_wheel(1,s_r)

                time.sleep(0.1)     

        time.sleep(0.01)

    print "stop the robot"

        

def behavior_3steps():

    S_t = 30 # wheel speed

    T_r = 30 # turning radius - smaller will track close to curve, but oscillate 

    b2 = 20 # half distance between two wheels in mm


    while not gQuit:

        if (len(gRobotList) > 0):

            if (gState == "3steps"):

                robot = gRobotList[0]


                floor_l = robot.get_floor(0)

                floor_r = robot.get_floor(1)

                sensor_diff = floor_l - floor_r

                print "Left:" + str(floor_l)+ " Right:"+ str(floor_r)+ "Diff:" +str(sensor_diff) 


                if (sensor_diff < -2): #steer left

                    s_l = S_t*(T_r-b2)/(T_r+b2)

                    s_r = S_t

                elif (sensor_diff > 2):

                    s_r = S_t*(T_r-b2)/(T_r+b2)

                    s_l = S_t

                else:

                    s_l = s_r = S_t

                robot.set_wheel(0,s_l)

                robot.set_wheel(1,s_r)
                time.sleep(0.1)

        time.sleep(0.01)

    print "stop the robot"

        

def behavior_p_controller():

    S_t = 30 # wheel speed

    T_r = 30 # turning radius - smaller will track close to curve, but oscillate 

    b2 = 20 # half distance between two wheels in mm

    Kp = .98



    while not gQuit:

        if (gState == "P"):

           if (len(gRobotList) > 0):

                robot = gRobotList[0]

                floor_l = robot.get_floor(0)

                floor_r = robot.get_floor(1)

                sensor_diff = floor_l - floor_r

                #T_r = int(round(190 / abs(Kp * sensor_diff + .01)))
                T_r = int(abs(Kp * sensor_diff))
                print "diff:",sensor_diff," T_r:",T_r
                # print "floor l, r", floor_l, floor_r, sensor_diff

                if (sensor_diff < 0): #steer left

                    s_l = S_t*(T_r-b2)/(T_r+b2)

                    s_r = S_t

                elif (sensor_diff > 0):

                    s_r = S_t*(T_r-b2)/(T_r+b2)

                    s_l = S_t

                else:

                    s_l = s_r = S_t

                robot.set_wheel(0,s_l)

                robot.set_wheel(1,s_r)

                time.sleep(0.01)     

        time.sleep(0.01)

    print "stop the robot"


def behavior_pi_controller():

    S_t = 30 # wheel speed

    T_r = 30 # turning radius - smaller will track close to curve, but oscillate 

    b2 = 20 # half distance between two wheels in mm

    Kp = .2
    
    while not gQuit:

        if (gState == "PI"):

           if (len(gRobotList) > 0):

                robot = gRobotList[0]

                floor_l = robot.get_floor(0)

                floor_r = robot.get_floor(1)

                sensor_diff = floor_l - floor_r

                T_r = int(round(190 / abs(Kp * sensor_diff + .01)))
                
                print "diff:",sensor_diff," T_r:",T_r
                # print "floor l, r", floor_l, floor_r, sensor_diff

                if (sensor_diff < 0): #steer left

                    s_l = S_t*(T_r-b2)/(T_r+b2)

                    s_r = S_t

                elif (sensor_diff > 0):

                    s_r = S_t*(T_r-b2)/(T_r+b2)

                    s_l = S_t

                else:

                    s_l = s_r = S_t

                robot.set_wheel(0,s_l)

                robot.set_wheel(1,s_r)

                time.sleep(0.01)     

        time.sleep(0.01)

    print "stop the robot"


def behavior_pid_controller():
    global gQuit
    error = []
    start = datetime.now()
    while not gQuit:

        if (len(gRobotList) > 0):

            if (gState == "PID"):

                robot = gRobotList[0]
                floor_l = robot.get_floor(0)
                floor_r = robot.get_floor(1)
                sensor_diff = floor_l - floor_r
                error.append(sensor_diff)
                print int(start-datetime.now())
                if(start-datetime.now()>=10 ):
                    print "Sum: ", sum(error),"Num: ", len(error),"e/s: ", len(error)/10,"e/t: ", sum(error)/10 
                    gQuit = True
                
                time.sleep(.01)

        time.sleep(0.01)

    print "stop the robot"



def TwoSteps(event=None):

    global gState

    gState = "2steps"



def ThreeSteps(event=None):

    global gState

    gState = "3steps"



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

  

    behavior_thread1 = threading.Thread(target=behavior_2steps)

    behavior_thread1.daemon = True

    behavior_thread1.start()



    # start a behavior tread

    behavior_thread2 = threading.Thread(target=behavior_3steps)

    behavior_thread2.daemon = True

    behavior_thread2.start()

    

    behavior_thread3 = threading.Thread(target=behavior_p_controller)

    behavior_thread3.daemon = True

    behavior_thread3.start()    



    behavior_thread4 = threading.Thread(target=behavior_pi_controller)

    behavior_thread4.daemon = True

    behavior_thread4.start()



    behavior_thread5 = threading.Thread(target=behavior_pid_controller)

    behavior_thread5.daemon = True

    behavior_thread5.start()



    button1 = tk.Button(frame,text="2Steps")

    button1.pack(side='left')

    button1.bind('<Button-1>', TwoSteps)

 

    button2 = tk.Button(frame,text="3Steps")

    button2.pack(side='left')

    button2.bind('<Button-1>', ThreeSteps)

 

    button3 = tk.Button(frame,text="P")

    button3.pack(side='left')

    button3.bind('<Button-1>', P_controller)

 

    button4 = tk.Button(frame,text="PI")

    button4.pack(side='left')

    button4.bind('<Button-1>', PI_controller)

 

    button5 = tk.Button(frame,text="PID")

    button5.pack(side='left')

    button5.bind('<Button-1>', PID_controller)

 

    button6 = tk.Button(frame,text="Exit")

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

    #sys.exit(main())

    main()