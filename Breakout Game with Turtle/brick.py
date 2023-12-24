from turtle import Turtle
from random import choice

COLORS = ['red', 'cyan', 'green', 'purple', 'orange', 'yellow', 'crimson']


class Brick(Turtle):
    def __init__(self):
        super().__init__()
        self.color(choice(COLORS))
        self.shape('square')
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.penup()
        self.start_x = -220
        self.start_y = 250
        self.gap = 3

    def disappear(self):
        self.goto(x=4000, y=4000)
