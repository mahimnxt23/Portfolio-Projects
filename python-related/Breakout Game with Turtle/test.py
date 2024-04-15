# TODO-1, install required packages...
import time
from turtle import *
from random import choice


# - - - - - - - - - - - - - - - - - - - - - - - - - SETUP PARTS - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# TODO-2, setup the game interface...
screen = Screen()
screen.title('Breakout Cloned with Turtle')
screen.setup(width=480, height=720)
screen.bgcolor('black')
screen.tracer(0)


# TODO-3, setup the handle/paddle used to direct the ball...
paddle = Turtle()
paddle.penup()
paddle.goto(x=0, y=(-340))
paddle.color('white')
paddle.shape('square')
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.speed(0)


# TODO-4, setup the ball (center of attraction)...
ball = Turtle()
ball.penup()
ball.goto(x=0, y=0)
ball.color('white')
ball.shape('circle')
ball.dx = 2
ball.dy = -2
ball.speed(100)


# TODO-5, setup the bricks...
colors = ['red', 'cyan', 'green', 'purple', 'orange']
bricks = []

brick_gap = 3
start_x = -220
start_y = 250

for row in range(6):  # originally value was 5...
    for column in range(11):

        brick = Turtle()
        brick.color(choice(colors))
        brick.shape('square')
        brick.shapesize(stretch_wid=1, stretch_len=2)
        brick.penup()
        brick.goto(
            start_x + column * (brick_gap + brick.shapesize()[1] * 20),
            start_y - row * (brick_gap + brick.shapesize()[0] * 20)
        )
        brick.speed(0)
        bricks.append(brick)


# - - - - - - - - - - - - - - - - - - - - - - - - - SETUP PARTS - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - LOGICAL PARTS - - - - - - - - - - - - - - - - - - - - - - - - - -

# TODO-6, finish handle/paddle movement functions...
def paddle_left():
    px = paddle.xcor()
    px -= 20
    if px > -220:
        paddle.setx(px)


def paddle_right():
    px = paddle.xcor()
    px += 20
    if px < 220:
        paddle.setx(px)


# TODO-7, use the functions from TODO-6 to bind keyboard keys for controlling...
screen.listen()
screen.onkey(paddle_left, 'a')
screen.onkey(paddle_left, 'Left')
screen.onkey(paddle_right, 'd')
screen.onkey(paddle_right, 'Right')

# TODO-8, make the game loop until game over...
game_is_on = True

while game_is_on:
    screen.update()

    # TODO-9, constantly move the ball...
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # TODO-10, check for border collision and bounce back in...
    if ball.xcor() < -230 or ball.xcor() > 220:
        ball.dx *= -1

    if ball.ycor() > 340:
        ball.dy *= -1

    # TODO-11, check ball and handle/paddle collision also set it's deflection direction...
    if ball.ycor() < -330 and (paddle.xcor() - 35 < ball.xcor() < paddle.xcor() + 35):
        ball.dy *= -1

    # TODO-12, check for brick and ball collision (another main attraction)...
    for brick in bricks:
        if brick.distance(ball) < 20 and -360 < brick.ycor() < 360:
            brick.goto(x=2000, y=2000)
            ball.dy *= -1

# TODO-13, implement and check for scores...


# TODO-14, manage force-quit or normal ways to breakout from the loop...


# - - - - - - - - - - - - - - - - - - - - - - - - - - LOGICAL PARTS - - - - - - - - - - - - - - - - - - - - - - - - - -
