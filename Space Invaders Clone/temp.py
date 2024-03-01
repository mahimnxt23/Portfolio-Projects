from turtle import Screen, Turtle
# from winsound import PlaySound, SND_ASYNC


# general_speed = 0
border_range = (-300, -300)
border_thickness = 5
player_position = (0, -280)
player_move_distance = 15
enemy_starting_position = (-200, 280)
enemy_move_distance = 2
bullet_move_distance = 3


# - - - - - - - - - - - - - - - - - - - - - - - - - SCREEN SECTION - - - - - - - - - - - - - - - - - - - - - - - -
screen = Screen()
screen.setup(width=650, height=650)
screen.title("Space Invader Alike")
screen.bgcolor("black")
# screen.tracer(1)
# - - - - - - - - - - - - - - - - - - - - - - - - - SCREEN SECTION - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - BORDER SECTION - - - - - - - - - - - - - - - - - - - - - - - -
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
# - - - - - - - - - - - - - - - - - - - - - - - - - BORDER SECTION - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - PLAYER SECTION - - - - - - - - - - - - - - - - - - - - - - - -
player = Turtle()
player.speed(0)
player.penup()
player.color("purple")
player.shape("arrow")
player.setposition(player_position)
player.setheading(to_angle=90)


def player_moves_left():
    player_x_position = player.xcor()
    player_x_position -= player_move_distance

    players_boundary_limit = border_range[0] + 20
    if player_x_position <= players_boundary_limit:
        player_x_position = players_boundary_limit
    player.setx(player_x_position)


def player_moves_right():
    player_x_position = player.xcor()
    player_x_position += player_move_distance

    players_boundary_limit = abs(border_range[0]) - 20
    if player_x_position >= players_boundary_limit:
        player_x_position = players_boundary_limit
    player.setx(player_x_position)


# - - - - - - - - - - - - - - - - - - - - - - - - - PLAYER SECTION - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - BULLET SECTION - - - - - - - - - - - - - - - - - - - - - - - -
bullet = Turtle()
bullet.speed(0)
bullet.penup()
bullet.color("yellow")
bullet.shape("triangle")
bullet.shapesize(0.5, 0.5)
bullet.setheading(to_angle=90)
bullet.hideturtle()


def fire_bullet():
    shoot = True

    bullet_arming_point = (
        player.xcor(),
        (player.ycor() + 10),
    )  # appear just above the player...
    bullet.setposition(bullet_arming_point)
    bullet.showturtle()

    while shoot:
        bullet_y_position = bullet.ycor()
        bullet_y_position += bullet_move_distance
        bullet.sety(bullet_y_position)

        if bullet_y_position >= 275:
            # bullet.clear()
            bullet.hideturtle()
            shoot = False


# - - - - - - - - - - - - - - - - - - - - - - - - - BULLET SECTION - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - KEYBOARD BINDINGS - - - - - - - - - - - - - - - - - - - - - - - -
screen.listen()
screen.onkeypress(player_moves_left, "Left")
screen.onkeypress(player_moves_right, "Right")
screen.onkey(fire_bullet, "space")
# - - - - - - - - - - - - - - - - - - - - - - - - KEYBOARD BINDINGS - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - ENEMY SECTION - - - - - - - - - - - - - - - - - - - - - - - -
enemy_ufo = Turtle()
enemy_ufo.speed(0)
enemy_ufo.penup()
enemy_ufo.color("red")
enemy_ufo.shape("circle")
enemy_ufo.setposition(enemy_starting_position)


def move_enemy_ufo():
    global enemy_move_distance
    game_on = True
    
    while game_on:
        enemy_x_position = enemy_ufo.xcor()
        enemy_x_position += enemy_move_distance
        enemy_ufo.setx(enemy_x_position)
    
        if enemy_x_position >= 280 or enemy_x_position <= -280:
            enemy_y_position = enemy_ufo.ycor()
            enemy_y_position -= 20
            enemy_move_distance *= -1
    
            if enemy_y_position <= -280:
                enemy_ufo.setposition(enemy_starting_position)
            else:
                enemy_ufo.sety(enemy_y_position)


# - - - - - - - - - - - - - - - - - - - - - - - - - ENEMY SECTION - - - - - - - - - - - - - - - - - - - - - - - -


# while True:
#     move_enemy_ufo()
#     screen.update()

# screen.mainloop()
move_enemy_ufo()
screen.update()
