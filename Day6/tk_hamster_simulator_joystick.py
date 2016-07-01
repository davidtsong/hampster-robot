import Tkinter as tk  # using Python 3
import time  # sleep
from HamsterAPI.comm_usb import RobotComm
import math
import threading
from tk_hamster_simulator import *
import Queue

gMaxRobotNum = 1; # max number of robots to control
gRobotList = None
gQuit = False

def update_virtual_world(virtual_world):
    waiting_for_robot = True

    while waiting_for_robot and virtual_world.real_robot:
        if (len(gRobotList) > 0):
            robot = gRobotList[0] 
            robot.set_wheel_balance(127)
            waiting_for_robot = False
            print "connected to robot"
        else:
            print "waiting for robot to connect"
        time.sleep(0.1)

    noise_prox = 25 # noisy level for proximity
    noise_floor = 20 #floor ambient color - if floor is darker, set higher noise
    prox_conv_l = [83, 82, 80, 71, 66, 56, 50, 44, 38, 34] #increment by 10mm sensor value
    prox_conv_r = [83, 83, 81, 73, 68, 57, 51, 45, 38, 34]

    d_factor = 1.0  #travel distance conversion
    b = 34 #distance between two wheels in mm

    vrobot = virtual_world.vrobot

    while (not gQuit):
        t = time.time()
        del_t = t - vrobot.t
        vrobot.t = t # update the tick
        ms = (vrobot.sl*del_t+vrobot.sr*del_t)/2 #speed of the center
        old_a = vrobot.a
        old_x = vrobot.x
        old_y = vrobot.y
        vrobot.a = vrobot.a + (vrobot.sl-vrobot.sr)*del_t/b
        vrobot.x = vrobot.x + ms * math.sin(vrobot.a) * d_factor
        vrobot.y = vrobot.y + ms * math.cos(vrobot.a) * d_factor
        if virtual_world.in_collision(vrobot.poly_id, rCanvas):
            vrobot.a = old_a
            vrobot.x = old_x
            vrobot.y = old_y

        while (vrobot.a >= 3.1415):
            vrobot.a -= 6.283

        #update sensors
        if (virtual_world.real_robot):
            robot = virtual_world.real_robot
            prox_l = robot.get_proximity(0)
            prox_r = robot.get_proximity(1)
            # convert sensor reading into distance to object detected
            if (prox_l > noise_prox):
                i = 0
                while (prox_conv_l[i] > prox_l) and (i < 9):
                    i += 1
                vrobot.dist_l = i*10 + (prox_conv_l[i-1] - prox_l)*10/(prox_conv_l[i-1] - prox_conv_l[i])
            else:
                vrobot.dist_l = False

            if (prox_r > noise_prox):
                i = 0
                while (prox_conv_r[i] > prox_r) and (i < 9):
                    i += 1
                vrobot.dist_r = i*10 + (prox_conv_r[i-1]-prox_r)*10/(prox_conv_r[i-1] - prox_conv_r[i])
            else:
                vrobot.dist_r = False
        else: #simulated robot
            virtual_world.get_vrobot_prox("left")
            virtual_world.get_vrobot_prox("right")

        if (virtual_world.real_robot):
            vrobot.floor_l = robot.get_floor(0)
            vrobot.floor_r = robot.get_floor(1)
        else:
            vrobot.floor_l = 100 #white
            vrobot.floor_r = 100

        time.sleep(0.05)

def draw_virtual_world(virtual_world):
    while (not gQuit):
        virtual_world.draw_robot()
        virtual_world.draw_prox("left")
        virtual_world.draw_prox("right")
        virtual_world.draw_floor("left")
        virtual_world.draw_floor("right")
        time.sleep(0.1)

def test_avoidance(virtual_world):
    moving = False
    vrobot = virtual_world.vrobot
    print "goto thread started: ", vrobot

    while not gQuit:
        if (virtual_world.go): 
            p_l = vrobot.dist_l
            p_r = vrobot.dist_r
            if (not p_l): # nothing in front
                p_l = 100
            if (not p_r): # nothing in front
                p_r = 100
            if (p_l > 65 and p_r > 65): # free to move remember now the sensor data is distance in mm
                vrobot.sl = 30
                vrobot.sr = 30 # moving forward
            else: # avoid obstalces
                vrobot.sl = 15
                vrobot.sr = 45
            robot = virtual_world.real_robot
            if robot:
                print "moving robot"
                robot.set_wheel(0,vrobot.sl)
                robot.set_wheel(1,vrobot.sr)
            moving = True
        else:
            if (moving):
                moving = False
                vrobot.sl = 0
                vrobot.sr = 0
                robot = virtual_world.real_robot
                if (robot):
                    robot.set_wheel(0,0)
                    robot.set_wheel(1,0)     
        time.sleep(0.1)
    print "goto stop"    

def stopProg(event=None):
    m.quit()
    gQuit = True
    print "Exit"

def drawGrid(event=None):
    print "draw Grid"
    canvas_width = vWorld.canvas_width
    canvas_height = vWorld.canvas_height
    x1 = 0
    x2 = canvas_width*2
    y1 = 0
    y2 = canvas_height*2
    del_x = 20
    del_y = 20
    num_x = x2 / del_x
    num_y = y2 / del_y
    # draw center (0,0)
    rCanvas.create_rectangle(canvas_width-3,canvas_height-3,canvas_width+3,canvas_height+3, fill="red")
    # horizontal grid
    for i in range (0,num_y):
        y = i * del_y
        rCanvas.create_line(x1, y, x2, y, fill="yellow")
    # verticle grid
    for j in range (0, num_x):
        x = j * del_x
        rCanvas.create_line(x, y1, x, y2, fill="yellow")

def drawMap(event=None):
    vWorld.draw_map()
    print vWorld.map, " map"

def clearCanvas(event=None):
    rCanvas.delete("all")
    poly_points = [0,0,0,0,0,0,0,0]
    vRobot.poly_id = rCanvas.create_polygon(poly_points, fill='blue')
    vRobot.prox_l_id = rCanvas.create_line(0,0,0,0, fill="red")
    vRobot.prox_r_id = rCanvas.create_line(0,0,0,0, fill="red")
    vRobot.floor_l_id = rCanvas.create_oval(0,0,0,0, outline="white", fill="white")
    vRobot.floor_r_id = rCanvas.create_oval(0,0,0,0, outline="white", fill="white")

def resetvRobot(event=None):
    #vRobot.reset_robot()
    vWorld.vrobot.x = 200
    vWorld.vrobot.y = 0
    vWorld.vrobot.a = -1.571
    vWorld.goal_achieved = True
    vWorld.goal_list_index = 0

def toggleTrace(event=None):
    if vWorld.trace == True:
        vWorld.trace = False
        button4["text"] = "Trace"
    else:
        vWorld.trace = True
        button4["text"] = "No Trace"

def toggleProx(event=None):
    if vWorld.prox_dots == True:
        vWorld.prox_dots = False
        button5["text"] = "Prox Dots"
    else:
        vWorld.prox_dots = True
        button5["text"] = "No Prox Dots"

def toggleFloor(event=None):
    if vWorld.floor_dots == True:
        vWorld.floor_dots = False
        button6["text"] = "Floor Dots"
    else:
        vWorld.floor_dots = True
        button6["text"] = "No Floor Dots"

def toggleRobot(event=None):
    if vWorld.real_robot:
        robot = vWorld.real_robot
        robot.set_wheel(0,0)
        robot.set_wheel(1,0)
        vWorld.real_robot = False
        print "simulated robot"
        button11["text"] = "Real Robot"
    else:
        if (len(gRobotList) > 0):
            vWorld.real_robot = gRobotList[0]
            robot = vWorld.real_robot
            robot.set_wheel(0,vWorld.vrobot.sl)
            robot.set_wheel(1,vWorld.vrobot.sr) 
            button11["text"] = "Simulation"
            print "connected to robot", vWorld.real_robot
        else:
            print "please turn on robot"

def toggleGo(event=None):
    if vWorld.go:
        vWorld.go = False
        print "Pause"
        button8["text"] = "Go"
    else:
        vWorld.go = True
        print "Go"
        button8["text"] = "Pause"

def getGoal(event):
    vWorld.canvas.create_oval(event.x-4, event.y-4, event.x+4, event.y+4, outline = "blue")
    canvas_width = vWorld.canvas_width
    canvas_height = vWorld.canvas_height
    vWorld.goal_x = event.x - canvas_width
    vWorld.goal_y = canvas_height - event.y 
    print "selected goal: ", vWorld.goal_x, vWorld.goal_y

def print_proximity(event=None):
    robot = vWorld.real_robot
    if robot:
        p_l = robot.get_proximity(0)
        p_r = robot.get_proximity(1)
        print p_l, p_r

def move_up(event=None):
    vWorld.vrobot.sl = 30
    vWorld.vrobot.sr = 30
    robot = vWorld.real_robot
    if robot:
        p_l = robot.get_proximity(0)
        p_r = robot.get_proximity(1)
        print p_l, p_r
        robot.set_wheel(0,vWorld.vrobot.sl)
        robot.set_wheel(1,vWorld.vrobot.sr)
    time.sleep(0.1)

def move_down(event=None):
    vWorld.vrobot.sl = -30
    vWorld.vrobot.sr = -30
    robot = vWorld.real_robot
    if robot:
        robot.set_wheel(0,vWorld.vrobot.sl)
        robot.set_wheel(1,vWorld.vrobot.sr)

def move_left(event=None):
    vWorld.vrobot.sl = 20
    vWorld.vrobot.sr = 30
    robot = vWorld.real_robot
    if robot:
        robot.set_wheel(0,vWorld.vrobot.sl)
        robot.set_wheel(1,vWorld.vrobot.sr)

def move_right(event=None):
    vWorld.vrobot.sl = 30
    vWorld.vrobot.sr = 20
    robot = vWorld.real_robot
    if robot:
        robot.set_wheel(0,vWorld.vrobot.sl)
        robot.set_wheel(1,vWorld.vrobot.sr)

def stop_move(event=None):
    vWorld.vrobot.sl = 0
    vWorld.vrobot.sr = 0
    robot = vWorld.real_robot
    if robot:
        robot.set_wheel(0,vWorld.vrobot.sl)
        robot.set_wheel(1,vWorld.vrobot.sr)
def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))

# main
if __name__== "__main__":
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'
    waiting_for_robot = True
    ls_localize = False

    gRobotList = comm.robotList
    #if don't want to connect to real robot
    #gRobotList = []
    m = tk.Tk() #root

    m.bind('<Motion>', motion)

    vRobot = virtual_robot()
    vRobot.t = time.time()
    #creating tje virtual appearance of the robot
    canvas_width = 440 # half width
    canvas_height = 300 # half height
    rCanvas = tk.Canvas(m, bg="white", width=canvas_width*2, height= canvas_height*2)
    rCanvas.pack()

    # visual elements of the virtual robot 
    poly_points = [0,0,0,0,0,0,0,0]
    vRobot.poly_id = rCanvas.create_polygon(poly_points, fill='blue') #robot
    vRobot.prox_l_id = rCanvas.create_line(0,0,0,0, fill="red") #prox sensors
    vRobot.prox_r_id = rCanvas.create_line(0,0,0,0, fill="red")
    vRobot.floor_l_id = rCanvas.create_oval(0,0,0,0, outline="white", fill="white") #floor sensors
    vRobot.floor_r_id = rCanvas.create_oval(0,0,0,0, outline="white", fill="white")
    time.sleep(1)

    #create the virtual worlds that contains the virtual robot
    vWorld = virtual_world()
    vWorld.vrobot = vRobot
    vWorld.canvas = rCanvas
    vWorld.canvas_width = canvas_width
    vWorld.canvas_height = canvas_height
    #objects in the world
    vWorld.map = []

    #bounder of board
    rect1 = [-100, -180, 0, -140]
    rect2 = [-140, -180, -100, -80]
    rect3 = [-100, 140, 0, 180]
    rect4 = [-140, 80, -100, 180]
    rect5 = [0, -50, 40, 50]
    rect6 = [-260, -20, -220, 20]
    rect7 = [40, 60, 140, 100]

    vWorld.area = [-300,-200,300,200]

    vWorld.add_obstacle(rect1)
    vWorld.add_obstacle(rect2)
    vWorld.add_obstacle(rect3)
    vWorld.add_obstacle(rect4)
    vWorld.add_obstacle(rect5)
    vWorld.add_obstacle(rect6)
    vWorld.add_obstacle(rect7)

  # set initial pose of robot
    vWorld.vrobot.x = 200
    vWorld.vrobot.y = 0
    vWorld.vrobot.a = 1.5*3.1415    

    update_vrobot_thread = threading.Thread(target=update_virtual_world, args=(vWorld,))
    update_vrobot_thread.daemon = True
    update_vrobot_thread.start()

    draw_world_thread = threading.Thread(target=draw_virtual_world, args=(vWorld,))
    draw_world_thread.daemon = True
    draw_world_thread.start()

    goto_thread = threading.Thread(target=test_avoidance, args=(vWorld,))
    goto_thread.daemon = True
    goto_thread.start()



    button0 = tk.Button(m,text="Grid")
    button0.pack(side='left')
    button0.bind('<Button-1>', drawGrid)

    button1 = tk.Button(m,text="Clear")
    button1.pack(side='left')
    button1.bind('<Button-1>', clearCanvas)

    button2 = tk.Button(m,text="Reset")
    button2.pack(side='left')
    button2.bind('<Button-1>', resetvRobot)

    button3 = tk.Button(m,text="Map")
    button3.pack(side='left')
    button3.bind('<Button-1>', drawMap)

    button4 = tk.Button(m,text="Trace")
    button4.pack(side='left')
    button4.bind('<Button-1>', toggleTrace)

    button5 = tk.Button(m,text="Prox Dots")
    button5.pack(side='left')
    button5.bind('<Button-1>', toggleProx)

    button6 = tk.Button(m,text="Floor Dots")
    button6.pack(side='left')
    button6.bind('<Button-1>', toggleFloor)


    button8 = tk.Button(m,text="Go")
    button8.pack(side='left')
    button8.bind('<Button-1>', toggleGo)

    button11 = tk.Button(m,text="Real Robot")
    button11.pack(side='left')
    button11.bind('<Button-1>', toggleRobot)

    button9 = tk.Button(m,text="Exit")
    button9.pack(side='left')
    button9.bind('<Button-1>', stopProg)

    rCanvas.bind_all('<w>', move_up)  
    rCanvas.bind_all('<s>', move_down)  
    rCanvas.bind_all('<a>', move_left)  
    rCanvas.bind_all('<d>', move_right)
    rCanvas.bind_all('<x>', stop_move)  

    rCanvas.bind_all('<p>', print_proximity)  
    m.mainloop()

    for robot in gRobotList:
        robot.reset()
    comm.stop()
    comm.join()

