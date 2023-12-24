from turtle import Turtle


class Paddle(Turtle):

    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.color('white')
        self.shape('square')
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.penup()
        self.goto(position)

    def paddle_left(self):
        px = self.xcor()
        px -= 20
        if px > -220:
            self.setx(px)

    def paddle_right(self):
        px = self.xcor()
        px += 20
        if px < 220:
            self.setx(px)
