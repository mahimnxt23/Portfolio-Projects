# TODO-1, install required packages...
import turtle as tim
import random


# - - - - - - - - - - - - - - - - - - - - - - - - - SETUP PARTS - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# TODO-2, setup the game interface...
window = tim.Screen()
window.title('Breakout Cloned with Turtle')
window.setup(width=480, height=720)
window.bgcolor('black')
# window.tracer()


# TODO-3, setup the handle/paddle used to direct the ball...
paddle = tim.Turtle()
paddle.penup()
paddle.goto(x=0, y=(-340))
paddle.color('white')
paddle.shape('square')
paddle.shapesize(stretch_wid=1, stretch_len=5)
# paddle.speed(0)


# TODO-4, setup the ball (center of attraction)...
ball = tim.Turtle()
ball.penup()
ball.goto(x=0, y=0)
ball.color('white')
ball.shape('circle')
ball.dx = 2
ball.dy = -2
# ball.speed(0)


# TODO-5, setup the bricks...
colors = ['red', 'blue', 'green', 'purple', 'orange']
bricks = []

for i in range(1):  # originally value was 5...
    for j in range(6):
        brick = tim.Turtle()
        brick.penup()
        brick.goto((-220 + (j * 90)), (220 - (i * 100)))  # this line is buggy...
        brick.color(random.choice(colors))
        brick.shape('square')
        brick.shapesize(stretch_wid=1, stretch_len=5)
        # brick.speed(100)
        bricks.append(brick)


# - - - - - - - - - - - - - - - - - - - - - - - - - SETUP PARTS - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - LOGICAL PARTS - - - - - - - - - - - - - - - - - - - - - - - - - -

# TODO-6, finish handle/paddle movement functions...


# TODO-7, use the functions from TODO-6 to bind keyboard keys for controlling...


# TODO-8, make the game loop until game over...


# TODO-9, constantly move the ball...


# TODO-10, check for border collision and bounce back in...


# TODO-11, check ball and handle/paddle collision also set it's deflection direction...


# TODO-12, check for brick and ball collision (another main attraction)...


# TODO-13, implement and check for scores...


# TODO-14, manage force-quit or normal ways to breakout from the loop...

# - - - - - - - - - - - - - - - - - - - - - - - - - - LOGICAL PARTS - - - - - - - - - - - - - - - - - - - - - - - - - -

window.mainloop()
