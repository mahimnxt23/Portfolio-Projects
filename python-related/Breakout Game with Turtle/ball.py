from turtle import Turtle


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.shape('circle')
        self.penup()
        self.goto(x=0, y=0)
        self.dx = 2
        self.dy = -2
        self.speed(10)

    def move(self):
        new_x = self.xcor() + self.dx
        new_y = self.ycor() + self.dy
        self.goto(new_x, new_y)

    def bounce_x(self):
        self.dx *= -1
        
    def bounce_y(self):
        self.dy *= -1
