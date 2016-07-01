import Queue
import Tkinter as tk

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
        self.queue = Queue.Queue()
        #self.lifo_queue = Queue.LifoQueue()
        self.priority_queue = Queue.PriorityQueue()
        self.canvas = canvas
        self.node_dist = 60
        self.node_size = 20

    def draw_node(self, a_node, n_color):
        if a_node.data: # coordinate to draw
          x = a_node.data[0]
          y = a_node.data[1]
          canvas = self.canvas
          dist = self.node_dist
          size = self.node_size
          canvas.create_oval(x*dist-size, y*dist-size, x*dist+size, y*dist+size, fill=n_color)
          canvas.create_text(x*dist, y*dist,fill="white",text=a_node.name)

    def draw_edge(self, node1, node2, e_color):
      if (node1.data and node2.data):
          x1 = node1.data[0]
          y1 = node1.data[1]
          x2 = node2.data[0]
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

        self.nodes[name].f_cost = 0
        self.priority_queue.put((0,self.nodes[name].name))

    def set_goal(self, name):
        self.goalNode = name
        self.draw_node(self.nodes[name], "green")

    def add_edge(self, node1, node2, g_cost):
        self.nodes[node1].edges.append([node2, g_cost])
        self.nodes[node2].edges.append([node1, g_cost])
        self.draw_edge(self.nodes[node1], self.nodes[node2], "blue")

    def dijk(self):
      lowest_cost = None
      print "Dijkstra's algorithm"
      while not self.priority_queue.empty():
        item = self.priority_queue.get()
        print "Item : " , item  

        current_node = self.nodes[item[1]]
        if(current_node.closed!= True):
          for edge in current_node.edges:
            a_node_name = edge[0]
            print "A node dest: ", a_node_name, " An edge", edge
            if not self.nodes[a_node_name].closed:
              # print "A node : ", a_node_name, " Current : ", current_node
              
              self.nodes[a_node_name].f_cost = self.nodes[current_node.name].f_cost + edge[1]
              print "cost: ", self.nodes[a_node_name].f_cost
              self.priority_queue.put((edge[1],a_node_name))
              self.nodes[a_node_name].back_pointer = current_node

              if a_node_name == self.goalNode:
                print "found path to ", a_node_name
                path = [a_node_name]
                if lowest_cost is None or self.nodes[a_node_name].f_cost < lowest_cost:
                  lowest_cost=path_cost = self.nodes[a_node_name].f_cost
                  path_node = self.nodes[a_node_name]

                  while path_node.back_pointer != False:
                    self.draw_edge(path_node, path_node.back_pointer, "yellow")
                    path_node = path_node.back_pointer
                    path.append(path_node.name)

                  if not self.path:
                    self.path = path
                    self.path.reverse()
                    print "path : ", self.path, "cost: ", path_cost
                else: print "Not small enough"
        current_node.closed = True
        # if(current_node.closed!=True):
        #   for an_edge in current_node.edges:
        #     a_node_name = an_edge[0]
        #     if not self.nodes[a_node_name].closed:
        #       self.priority_queue.put(an_edge[1],a_node_name)
        #       print "put queue: ", a_node_name
        #       self.nodes[a_node_name].back_pointer = current_node
        #       if a_node_name == self.goalNode:
        #         print "found path to ", a_node_name
        #         path = [a_node_name]
        #         #path_cost = 0
        #         path_node = self.nodes[a_node_name]
        #         while path_node.back_pointer != False:
        #           self.draw_edge(path_node, path_node.back_pointer, "yellow")
        #           path_node = path_node.back_pointer
        #           path.append(path_node.name)

        #         if not self.path:
        #           self.path = path
        #           self.path.reverse()
        #           print "path: ", self.path
        #     else:
        #       print "node closed: ", a_node_name
        # current_node.closed = True

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
                  path_node = path_node.back_pointer
                  path.append(path_node.name)

                if not self.path:
                  self.path = path
                  self.path.reverse()
                  print "path: ", self.path
            else:
              print "node closed: ", a_node_name
        current_node.closed = True


def main():

    frame = tk.Tk()

    canvas = tk.Canvas(frame, bg="white", width=300, height=300)
    canvas.pack(expand=1, fill='both')

    print "created graph"
    MyGraph = Graph(canvas)

    # Node_ = MyGraph.add_node("A", [1,1])
    # Node_ = MyGraph.add_node("B", [2,1])
    # Node_ = MyGraph.add_node("C", [2,2])
    # Node_ = MyGraph.add_node("D", [1,2])
    
    # MyGraph.add_edge("A","B",1)
    # MyGraph.add_edge("B","D",1)
    # MyGraph.add_edge("B","C",1)
    # MyGraph.add_edge("C","D"  ,1)

    # MyGraph.set_start("A")
    # MyGraph.set_goal("D")
    Node_S = MyGraph.add_node("S", [2,1])
    Node_A = MyGraph.add_node("A", [1,2])
    Node_B = MyGraph.add_node("B", [2,2])
    Node_C = MyGraph.add_node("C", [3,2])
    Node_D = MyGraph.add_node("D", [2,3])

    MyGraph.set_start("S")
    MyGraph.set_goal("D")

    MyGraph.add_edge("A", "S", 3)
    MyGraph.add_edge("B", "S", 3)
    MyGraph.add_edge("C", "S", 2)
    MyGraph.add_edge("B", "D", 1)
    MyGraph.add_edge("A", "D", 5)
    MyGraph.add_edge("C", "D", 3)

    MyGraph.dijk()

    frame.mainloop()


if __name__ == "__main__":
    main()