class Node:
    def __init__(self, app, x, y):
        self.app = app
        # coordinates in a grid
        self.x = x
        self.y = y
        # what's drawn on a screen
        self.rectangle = self.app.canvas.create_rectangle(
            self.x * self.app.cell_size,
            self.y * self.app.cell_size,
            (self.x + 1) * self.app.cell_size,
            (self.y + 1) * self.app.cell_size,
            outline='black'
        )
        # for pathfinding
        self.parent = None
        self.g = None
        self.h = None
        self.f = None
        self.obstacle = False
    
    def __repr__(self):
        # when printing an instance of the class
        return f'{self.x} {self.y}'
    
    def change_color(self, color):
        # changes color to the color specified
        self.app.canvas.itemconfig(self.rectangle, fill=color)