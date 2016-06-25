import time
import Tkinter as tk
import threading
import Queue

class State:
    def __init__(self):
      self.name = ''
      self.coords = [0,0]
      self.transitions = {} #dictionary

    def add_transition(self, event_name, toState, callback):
      self.transitions[event_name] = [toState, callback]

class StateMachine:
    def __init__(self):
        self.states = {}
        self.startState = None
        self.currentState = None
        self.canvas = None

    def add_state(self, name, x, y):
        a_state = State()
        a_state.name = name
        a_state.coords = [x,y]
        self.states[name] = a_state
        return a_state

    def set_start(self, name):
        self.startState = name

    def set_current(self, name):
        self.currentState = name

    def draw_state(self, name, rcolor):
        size_x = 20 
        size_y = 20
        a_state = self.states[name]
        x = a_state.coords[0]
        y = a_state.coords[1]
        canvas = self.canvas
        canvas.create_rectangle(x+size_x, y+size_y, x, y, fill=rcolor)
        canvas.create_text(x+size_x/2, y+size_y/2,fill="darkblue",text=name)

    def run(self, q):
        if not q.empty():
          state = self.states[self.currentState] 
          print "current state", state.name
          char_pressed = q.get()
          if state.transitions.has_key(char_pressed):
            transition = state.transitions[char_pressed]
            if (transition[1] != False):
              transition[1]()
            self.draw_state(state.name,"yellow")
            self.currentState = transition[0]
            s_name = self.currentState
            self.draw_state(s_name,"green")

def moving_to_A(): #callback function when transition from B to A
  print "moving to A"

def moving_to_B():
  print "moving to B" #callback function when transition from A to B

def mymachine_behavior(q):
    global frame

    MyStateMachine = StateMachine()
    print "created a state machine"

    MyStateMachine.canvas = canvas
    State_A = MyStateMachine.add_state("A", 100, 150)
    MyStateMachine.draw_state("A", "yellow")
    State_B = MyStateMachine.add_state("B", 200, 150)
    MyStateMachine.draw_state("B", "yellow")

    MyStateMachine.set_start("A")
    MyStateMachine.set_current("A")
    MyStateMachine.draw_state(MyStateMachine.currentState,"green")

    State_A.add_transition("b_pressed", "B", moving_to_B)
    State_B.add_transition("a_pressed", "A", moving_to_A)

    while (True):
      MyStateMachine.run(q)

    print "State Machine Finished"

def a_pressed(event=None):
  print "a pressed"
  q.put("a_pressed")

def b_pressed(event=None):
  print "b pressed"
  q.put("b_pressed")

def main():
    global frame, canvas
    global q

    q = Queue.Queue()

    frame = tk.Tk()

    canvas = tk.Canvas(frame, bg="white", width=300, height=300)
    canvas.pack(expand=1, fill='both')

    canvas.bind_all("<a>", a_pressed)
    canvas.bind_all("<b>", b_pressed)

    behavior_thread = threading.Thread(target=mymachine_behavior, args=(q,))
    behavior_thread.daemon = True
    behavior_thread.start()

    frame.mainloop()

if __name__ == "__main__":
    main()