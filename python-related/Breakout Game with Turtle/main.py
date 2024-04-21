from turtle import Screen
from paddle import Paddle
from ball import Ball
from brick import Brick
from scoreboard import Scoreboard
from time import sleep
from tkinter import TclError


# UI setup...
screen = Screen()
screen.title('Breakout Cloned with Turtle')
screen.bgcolor('black')
screen.setup(width=480, height=720)
screen.tracer(0)

# initiate all packages...
paddle = Paddle((0, -340))
ball = Ball()
score = Scoreboard()


# create the bricks...
bricks = []
for row in range(8):
    for column in range(11):
        brick = Brick()

        brick.goto(
            brick.start_x + column * (brick.gap + brick.shapesize()[1] * 20),
            brick.start_y - row * (brick.gap + brick.shapesize()[0] * 20)
        )
        bricks.append(brick)


# start listening for key presses...
screen.listen()
screen.onkey(paddle.paddle_left, 'a')
screen.onkey(paddle.paddle_left, 'Left')
screen.onkey(paddle.paddle_right, 'd')
screen.onkey(paddle.paddle_right, 'Right')


total_hits = 0
game_is_on = True
while game_is_on:

    try:
        screen.update()  # update screen all the time...
        score.update_scoreboard()  # showcase scoreboard all the time...
        ball.move()  # start moving the ball...

        if ball.xcor() < -230 or ball.xcor() > 220:  # checks sidebar collision and bounces back in...
            ball.bounce_x()

        if ball.ycor() > 340:  # checks upper bar collision and bouncing back in...
            ball.bounce_y()

        if ball.ycor() < -340:  # checks down bar collision, deduct life and reset ball position...
            score.deduct_lives()
            sleep(0.5)  # adds a pause to react...
            ball.goto(0, 0)
            ball.move()  # starting ball movement again...

        # checks collision with paddle and bouncing back up...
        if ball.ycor() < -330 and (paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50):
            ball.bounce_y()

        if score.remaining_lives == 0:  # checks if Game Over needs to shown...
            score.show_game_over()
            # ball.goto(0, 0)
            # sleep(5)
            game_is_on = False

        if total_hits == len(bricks):  # checks if Congratulations needs to shown...
            score.show_congrats()
            # sleep(3)
            game_is_on = False

        for block in bricks:  # constantly look for hits with brick and update all proprieties...
            if block.distance(ball) < 20 and -360 < block.ycor() < 360:
                score.add_score()
                total_hits += 1
                block.disappear()
                ball.bounce_y()

    except TclError:  # this error just randomly pops up sometimes, so silencing it...
        pass


screen.exitonclick()
