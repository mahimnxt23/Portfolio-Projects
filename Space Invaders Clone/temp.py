# import os
from turtle import Screen, Turtle

# from winsound import PlaySound, SND_ASYNC


# general_speed = 0
border_range = (-300, -300)
border_thickness = 5
player_position = (0, -280)
player_move_distance = 15


# screen setup...
screen = Screen()
screen.setup(width=650, height=650)
screen.title("Space Invader Alike")
screen.bgcolor("black")

# border setup...
border = Turtle()
border.speed(0)
border.color("white")
border.hideturtle()
border.penup()
border.setposition(border_range)
border.pendown()
border.pensize(border_thickness)

for each_side in range(4):
    border.fd(600)
    border.lt(90)


# player setup...
player = Turtle()
player.speed(0)
player.penup()
player.color("purple")
player.shape("arrow")
player.setposition(player_position)
player.setheading(to_angle=90)


# player movement setup...
def move_left():
    player_x_position = player.xcor()
    player_x_position -= player_move_distance

    players_boundary_limit = border_range[0] + 20
    if player_x_position <= players_boundary_limit:
        player_x_position = players_boundary_limit
    player.setx(player_x_position)


def move_right():
    player_x_position = player.xcor()
    player_x_position += player_move_distance

    players_boundary_limit = abs(border_range[0]) - 20
    if player_x_position >= players_boundary_limit:
        player_x_position = players_boundary_limit
    player.setx(player_x_position)


# keyboard bindings...
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")


screen.mainloop()
