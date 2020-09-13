import tkinter as tk
from node import Node
import math

class App:
    def __init__(self):
        # root init
        self.root = tk.Tk()
        self.root.title('Pathfinding')
        # canvas settings
        self.width = 700
        self.height = 700
        self.cell_size = 50
        self.rows = self.width // self.cell_size
        self.cols = self.height // self.cell_size
        self.canvas = tk.Canvas(self.root, width=self.width,
                                height=self.height, bg='white')
        self.canvas.pack()
        self.nodes = self.create_grid()
        # open and closed list for pathfinding
        self.open = []
        self.closed = []
        # default start and end nodes
        self.start = None
        self.end = None
        self.set_start(self.nodes[0][0])
        self.set_end(self.nodes[-1][-1])
        # click does things, on_key set things for click to do, enter to start pf
        self.root.bind('<Button-1>', self.click)
        self.root.bind('<Return>', self.start_pathfinding)
        self.root.bind('<Key>', self.on_key)
        # clear all, set obstacle, clear obstacle, set start, set end
        self.events = [False, False, False, False, False]
        # binds
        self.chars = ['1', '2', '3', '4', '5']

    
    def create_grid(self):
        # creates grid of nodes
        nodes = []
        for x in range(self.cols):
            row = []
            for y in range(self.rows):
                node = Node(self, x, y)
                row.append(node)
            nodes.append(row)
        return nodes
    
    def start_pathfinding(self, event):
        # starts the pathfinding loop
        self.loop = self.root.after(200, self.find_path)
    
    def find_path(self):
        # finds path then backtracks it from the end trough parent nodes
        self.path = []

        if len(self.open) != 0:
            # finding a node with the lowest f
            current = self.open[0]
            for node in self.open:
                if node.f < current.f:
                    current = node

            self.open.remove(current)
            current.change_color('red')
            self.closed.append(current)
            # end node found, time to backtrack the path
            if current == self.end:
                self.root.after_cancel(self.loop)
                self.path.append(self.end)
                self.backtrack_loop = self.root.after(50, self.backtrack)
                return
            # for each neighbour
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x = current.x + i
                    y = current.y + j
                    # out of x-border, skip
                    if x < 0 or x >= self.width // self.cell_size:
                        continue
                    # out of y-border, skip
                    if y < 0 or y >= self.height // self.cell_size:
                        continue
                    # self, skip
                    if x == 0 and y == 0:
                        continue
                    neighbour = self.nodes[x][y]
                    # if obstacle or in closed, skip
                    if neighbour in self.closed:
                        continue
                    if neighbour.obstacle:
                        continue
                    
                    # g -> path from the start to the neighbour; next = 10, diagonal = 14
                    temp_g = current.g + self.get_distance(current, neighbour)
                    # h -> path from the neighbour to the end; next = 10, diagonal = 14
                    temp_h = self.get_distance(neighbour, self.end)
                    # f -> total cost of g + f
                    temp_f = temp_g + temp_h
                    # if the current path to the neighbour is shorter
                    if neighbour.f != None and temp_f < neighbour.f or neighbour not in self.open:
                        neighbour.g = temp_g
                        neighbour.h = temp_h
                        neighbour.f = temp_f
                        # setting parent for backtracking
                        neighbour.parent = current
                        if neighbour not in self.open:
                            neighbour.change_color('green')
                            self.open.append(neighbour)
                    
            
            self.loop = self.root.after(200, self.find_path)

        else:
            self.root.after_cancel(self.loop)
        
    def get_distance(self, start, end):
        # aligns vertically/horizontally, then horizontal/vertical steps, next = 10, diagonal = 14
        dx = abs(start.x - end.x)
        dy = abs(start.y - end.y)

        if dx > dy:
            return 14*dy + 10*(dx - dy)
        return 14*dx + 10*(dy - dx)
    
    def backtrack(self):
        # goes from the end trough the parents until the root(start) is found
        node = self.path[-1]
        if node == None:
            self.root.after_cancel(self.backtrack_loop)
        else:
            node.change_color('blue')
            self.path.append(node.parent)
            self.backtrack_loop = self.root.after(50, self.backtrack)
    
    def click(self, event):
        # finds click coordinations in the grid
        clicked = self.nodes[event.x // self.cell_size][event.y // self.cell_size]

        if self.events[0]:
            # clearing all, setting default start/end
            for row in self.nodes:
                for node in row:
                    node.change_color('white')
                    node.obstacle = False
            self.open = []
            self.closed = []
            self.set_start(self.nodes[0][0])
            self.set_end(self.nodes[-1][-1])

        if self.events[1]:
            # setting obstacles
            clicked.obstacle = True
            clicked.change_color('black')
        
        if self.events[2]:
            # removing obstacles
            clicked.obstacle = False
            clicked.change_color('white')
        
        if self.events[3]:
            # setting start
            self.set_start(clicked)
        
        if self.events[4]:
            # setting end
            self.set_end(clicked)
    
    def on_key(self, event):
        # clears prev binds, binds key pressed if allowed
        char = event.char
        if char in self.chars:
            for i in range(len(self.events)):
                self.events[i] = False
            self.events[self.chars.index(char)] = True
    
    def set_start(self, node):
        # resets current start if any, sets new start
        if self.start == None:
            pass
        else:
            self.start.g = None
            self.start.f = None
            self.start.change_color('white')
            if self.start in self.open:
                self.open.remove(self.start)

        self.start = node
        self.start.g = 0
        self.start.f = 0
        self.open.append(self.start)
        self.start.change_color('blue')
    
    def set_end(self, node):
        # resets current end if any, sets new end
        if self.end != None:
            self.end.change_color('white')
        self.end = node
        self.end.change_color('blue')
        
        

app = App()
app.root.mainloop()
