import Queue
import Tkinter as tk
from random import randint

class Node:
    def __init__(self):
      self.name = ''
      self.data =[]
      self.f_cost = 0
      #self.h_cost = 0
      self.back_pointer = False
      self.closed = False
      self.edges = []
      self.visited = False

class Graph:
    def __init__(self, canvas):
        self.nodes = {}
        self.startNode = None
        self.goalNode = None
        self.path = []
        self.path_cost = False
        self.queue = Queue.Queue()
        self.lifo_queue = Queue.LifoQueue()
        #self.priority_queue = Queue.PriorityQueue()
        self.canvas = canvas
        self.node_dist = 80
        self.node_size = 30

    def draw_node(self, a_node, n_color):
        if a_node.data: # coordinate to draw
          x = a_node.data[0]
          y = a_node.data[1]
          canvas = self.canvas
          dist = self.node_dist
          size = self.node_size
          canvas.create_oval(x*dist-size, y*dist-size, x*dist+size, y*dist+size, fill=n_color)
          canvas.create_text(x*dist, y*dist,fill="black",text=a_node.name)

    def draw_edge(self, node1, node2, e_color):
      if (node1.data and node2.data):
          x1 = node1.data[0]
          y1 = node1.data[1]
          x2 = node2.data[0]
          y2 = node2.data[1]
          dist = self.node_dist
          canvas = self.canvas
          canvas.create_line(x1*dist, y1*dist, x2*dist, y2*dist, fill=e_color)
          #canvas.create_rectangle(x1*dist-2, y1*dist-2, x2*dist+2, y2*dist+2, fill=e_color, outline=e_color)

    def add_node(self, name, data):
        a_node = Node()
        a_node.name = name
        a_node.data = data
        self.nodes[name] = a_node
        self.draw_node(a_node, "white")
        return a_node

    def set_start(self, name):
        self.startNode = name
        self.draw_node(self.nodes[name], "red")
        self.queue.put(self.nodes[name])
        self.lifo_queue.put(self.nodes[name])

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
          #print "expand current node: ", current_node.name
          #print "edges from node: ",current_node.edges
          for an_edge in current_node.edges:
            a_node_name = an_edge[0]
            if not self.nodes[a_node_name].closed: #has been "expanded"
              self.queue.put(self.nodes[a_node_name])
              #print "put queue: ", a_node_name
              self.nodes[a_node_name].back_pointer = current_node

              # check if path to goal is found, if so, extract path
              if a_node_name == self.goalNode:
                #print "found path to ", a_node_name
                path = [a_node_name]
                #path_cost = 0
                path_node = self.nodes[a_node_name]
                while not self.path and path_node.back_pointer != False:
                  self.draw_edge(path_node, path_node.back_pointer, "yellow")
                  path_node = path_node.back_pointer
                  path.append(path_node.name)
                if not self.path:
                  self.path = path
                  self.path.reverse()
                  print "path: ", self.path
                
            else:
              pass
              #print "node closed: ", a_node_name
        current_node.closed = True
      return self.path

    def DFS(self):
      print "Depth First Search"
      while not self.lifo_queue.empty():
        current_node = self.lifo_queue.get()
        if (current_node.closed != True):
          print "expand current node: ", current_node.name
          print "edges from node: ",current_node.edges
          for an_edge in current_node.edges:
            a_node_name = an_edge[0]
            if not self.nodes[a_node_name].closed: #has been "expanded"
              self.lifo_queue.put(self.nodes[a_node_name])
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
                  path_node = path_node.back_pointer
                  path.append(path_node.name)
                if not self.path:
                  self.path = path
                  self.path.reverse()
                  print "path: ", self.path
                
            else:
              print "node closed: ", a_node_name
        current_node.closed = True
        

def create_grid(Graph, width, length, obstacles):
  for r in xrange(width):
    for c in xrange(length):
      name = str(r) + "-" + str(c)
      if not [r, c] in obstacles:
        Graph.add_node(name, [r+1, 5-c])

  for r in xrange(width):
    for c in xrange(length):
      name = str(r) + "-" + str(c)
      if name in Graph.nodes:
        if Graph.nodes[name].data[1] > 1:
          name2 = name[:-1] + str(int(name[-1]) + 1)
          if name2 in Graph.nodes:
            Graph.add_edge(name, name2, 1)
        if Graph.nodes[name].data[0] < width:
          name2 = str(int(name[0]) + 1) + name[1:]
          if name2 in Graph.nodes:
            Graph.add_edge(name, name2, 1)  
        

def main():

    frame = tk.Tk()

    canvas = tk.Canvas(frame, bg="white", width=400, height=400)
    canvas.pack(expand=1, fill='both')

    print "created graph"
    MyGraph = Graph(canvas)

    create_grid(MyGraph, 5, 4, [[0,1], [3,2]])

    MyGraph.set_start("0-0")
    MyGraph.set_goal("4-2")

    MyGraph.dijkstra()
    

    frame.mainloop()


if __name__ == "__main__":
    main()