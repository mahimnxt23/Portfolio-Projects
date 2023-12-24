from turtle import Screen
from paddle import Paddle
from ball import Ball
from brick import Brick
from scoreboard import Scoreboard
from time import sleep


screen = Screen()
screen.title('Breakout Cloned with Turtle')
screen.bgcolor('black')
screen.setup(width=480, height=720)
screen.tracer(0)

paddle = Paddle((0, -340))
ball = Ball()
score = Scoreboard()


bricks = []
for row in range(6):
    for column in range(11):
        brick = Brick()

        brick.goto(
            brick.start_x + column * (brick.gap + brick.shapesize()[1] * 20),
            brick.start_y - row * (brick.gap + brick.shapesize()[0] * 20)
        )
        bricks.append(brick)


screen.listen()
screen.onkey(paddle.paddle_left, 'a')
screen.onkey(paddle.paddle_left, 'Left')
screen.onkey(paddle.paddle_right, 'd')
screen.onkey(paddle.paddle_right, 'Right')


game_is_on = True
while game_is_on:
    screen.update()
    ball.move()

    if ball.xcor() < -230 or ball.xcor() > 220:
        ball.bounce_x()

    if ball.ycor() > 340:
        ball.bounce_y()

    if ball.ycor() < -330 and (paddle.xcor() - 35 < ball.xcor() < paddle.xcor() + 35):
        ball.bounce_y()

    for block in bricks:
        if block.distance(ball) < 20 and -360 < block.ycor() < 360:
            block.disappear()
            ball.bounce_y()
