import Queue
import time
def addCommand(currentDir, desiredDir):
    commandseg  = []
    if desiredDir - currentDir == 0:
        commandseg.append("forward()")
    if desiredDir - currentDir == -1:
        commandseg.append("left()")
        commandseg.append("forward()")
    if desiredDir - currentDir == 1:
        commandseg.append("right()")
        commandseg.append("forward()")
    if abs(desiredDir - currentDir) == 2:
        commandseg.append("right()")
        commandseg.append("right()")
        commandseg.append("forward()")
    if desiredDir - currentDir == -3:
        commandseg.append("right()")
        commandseg.append("forward()")
    if desiredDir - currentDir == 3:
        commandseg.append("left()")
        commandseg.append("forward()")
    return commandseg
def buildCommandQueue(pathraw,robot):
    turning = False
    path = []
    commands = []
    i = 0
    direction = None
    for i in range(len(pathraw)):
        pathraw[i].split("-")
        path.append([int(pathraw[i][0]),int(pathraw[i][2])])  
    print "The working : " ,path      
    for i in range(len(path)):
        if i != len(path)-1:
            nextCoord = path[i+1]
            currentCoord = path[i]

            if currentCoord[1]+1 == nextCoord[1]:#go right
                if direction is None: 
                    direction = 2
                commands = commands + addCommand(direction,2)
                direction = 2
            if currentCoord[1]-1 == nextCoord[1]:#go left
                if direction is None: 
                    direction = 4
                commands = commands + addCommand(direction,4)
                direction = 4
            if currentCoord[0]+1 == nextCoord[0]:#go up
                if direction is None: 
                    direction = 1
                commands = commands + addCommand(direction,1)
                direction = 1
            if currentCoord[0]-1 == nextCoord[0]:#go down
                if direction is None: 
                    direction = 3
                commands = commands + addCommand(direction,3)
                direction = 3
            print direction
            print commands
    print commands
    return commands
    print "done making commands"

class Node:
    def __init__(self):
      self.name = ''
      self.data =[]
      self.f_cost = 0
      #self.h_cost = 0
      self.back_pointer = False
      self.closed = False
      self.edges = []

class Graph:
    def __init__(self, canvas):
        self.nodes = {}
        self.startNode = None
        self.goalNode = None
        self.path = []
        #self.path_cost = False
        self.queue = Queue.LifoQueue()
        #self.lifo_queue = Queue.LifoQueue()
        #self.priority_queue = Queue.PriorityQueue()
        self.canvas = canvas
        self.node_dist = 60
        self.node_size = 20

    def draw_node(self, a_node, n_color):
        if a_node.data: # coordinate to draw
          x = a_node.data[0] + 1 #columns
          y = a_node.data[1] #rows
          canvas = self.canvas
          dist = self.node_dist
          size = self.node_size
          canvas.create_oval(x*dist-size, y*dist-size, x*dist+size, y*dist+size, fill=n_color)
          canvas.create_text(x*dist, y*dist,fill="white",text=a_node.name)

    def draw_edge(self, node1, node2, e_color):
      if (node1.data and node2.data):
          x1 = node1.data[0] + 1 #columns compensates for the drawn thing
          y1 = node1.data[1]
          x2 = node2.data[0] + 1 #columns compensates for the drawn thing
          y2 = node2.data[1]
          dist = self.node_dist
          canvas = self.canvas
          canvas.create_line(x1*dist, y1*dist, x2*dist, y2*dist, fill=e_color)

    def add_node(self, name, data):
        a_node = Node()
        a_node.name = name
        a_node.data = data
        self.nodes[name] = a_node
        self.draw_node(a_node, "blue")
        return a_node

    def set_start(self, name):
        self.startNode = name
        self.draw_node(self.nodes[name], "red")
        self.queue.put(self.nodes[name])

    def set_goal(self, name):
        self.goalNode = name
        self.draw_node(self.nodes[name], "green")

    def add_edge(self, node1, node2, g_cost):
        self.nodes[node1].edges.append([node2, g_cost])
        self.nodes[node2].edges.append([node1, g_cost])
        self.draw_edge(self.nodes[node1], self.nodes[node2], "blue")


    def BFS(self): # Breadth First Search
      print "Breadth First Search"
      while not self.queue.empty():
        current_node = self.queue.get()
        if (current_node.closed != True):
          print "expand current node: ", current_node.name
          print "edges from node: ",current_node.edges
          for an_edge in current_node.edges:
            a_node_name = an_edge[0]
            if not self.nodes[a_node_name].closed: #has been "expanded"
              self.queue.put(self.nodes[a_node_name])
              print "put queue: ", a_node_name
              self.nodes[a_node_name].back_pointer = current_node

              # check if path to goal is found, if so, extract path
              if a_node_name == self.goalNode:
                print "found path to ", a_node_name
                path = [a_node_name]
                #path_cost = 0
                path_node = self.nodes[a_node_name]
                while path_node.back_pointer != False:
                  self.draw_edge(path_node, path_node.back_pointer, "yellow")
                  print "Last : " + path_node.name
                  path_node = path_node.back_pointer
                  path.append(path_node.name)

                if not self.path:
                  self.path = path
                  self.path.reverse()
                  print "path: ", self.path
                  return self.path
            else:
              print "node closed: ", a_node_name
        current_node.closed = True
        print self.path
        

def draw_nodes(MyGraph, columns, rows):
  c = 0
  r = 0
  n = 0
  
  for r in range(rows):
    for c in range(columns):
      node_name = str(r)+"-"+str(c)
      MyGraph.add_node(node_name, [c, rows-r])
      if c > 0:
        MyGraph.add_edge(str(r)+"-"+str(c), str(r)+"-"+str(c-1),1)
      if r > 0:
        MyGraph.add_edge(str(r)+"-"+str(c), str(r-1)+"-"+str(c),1)


def closeNode(MyGraph, nodeName):
  node = MyGraph.nodes[nodeName]
  node.closed = True
  MyGraph.draw_node(node, "white")

