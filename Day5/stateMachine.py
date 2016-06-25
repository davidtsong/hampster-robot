#import sys
import Queue

class Event(object):
    def __init__(self, event_type, event_data):
      self.type = event_type #string
      self.data = event_data #list of number or character depending on type

class State:
    def __init__(self):
      self.name = ''
      self.transitions = {}

    def add_transition(self, event_type, toState, callback):
      self.transitions[event_type] = [toState, callback]

class StateMachine:
    def __init__(self):
        self.states = {}
        self.startState = None
        self.currentState = None

    def add_state(self, name):
        a_state = State()
        a_state.name = name
        self.states[name] = a_state
        return a_state

    def set_start(self, name):
        self.startState = name

    def set_current(self, name):
        self.currentState = name

    def get_state(self, name):
        return self.states[name]

    def run(self, robot, q):
      while not q.empty():
        event = q.get()
        state = self.states[self.currentState] 
        if state.transitions.has_key(event.type):
          transition = state.transitions[event.type]
        else:
          transition = False
        if transition:
          if (transition[1] != False):
            transition[1](robot)
          self.currentState = transition[0]
