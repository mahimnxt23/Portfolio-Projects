


# general_speed = 0
enemy_starting_position = (-200, 280)
 = 2
bullet_move_distance = 3
shoot = False
game_on = True

# - - - - - - - - - - - - - - - - - - - - - - - - - SCREEN SECTION - - - - - - - - - - - - - - - - - - - - - - - -


screen.bgcolor("black")
# screen.tracer(1)
# - - - - - - - - - - - - - - - - - - - - - - - - - SCREEN SECTION - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - BORDER SECTION - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - BORDER SECTION - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - PLAYER SECTION - - - - - - - - - - - - - - - - - - - - - - - -



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
    global shoot
    shoot = True

    bullet_arming_point = (
        player.xcor(),
        (player.ycor() + 10),
    )  # appear just above the player...
    bullet.setposition(bullet_arming_point)
    bullet.showturtle()

    if shoot:
        bullet_y_position = bullet_arming_point[1]
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
screen.onkeypress(fire_bullet, "space")
# - - - - - - - - - - - - - - - - - - - - - - - - KEYBOARD BINDINGS - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - ENEMY SECTION - - - - - - - - - - - - - - - - - - - - - - - -
enemy_ufo = Turtle()
enemy_ufo.speed(0)
enemy_ufo.penup()
enemy_ufo.color("red")
enemy_ufo.shape("circle")
enemy_ufo.setposition(enemy_starting_position)


def move_enemy_ufo():
    global enemy_move_distance, game_on

    if game_on:
        enemy_x_position = enemy_ufo.xcor()
        enemy_x_position += enemy_move_distance
        enemy_ufo.setx(enemy_x_position)

        if enemy_x_position >= 280 or enemy_x_position <= -280:
            enemy_y_position = enemy_ufo.ycor()
            enemy_y_position -= 20
            enemy_move_distance *= -1

            if enemy_y_position <= -280:
                enemy_ufo.setposition(enemy_starting_position)
                game_on = False
            else:
                enemy_ufo.sety(enemy_y_position)

        screen.ontimer(move_enemy_ufo, 10)
# - - - - - - - - - - - - - - - - - - - - - - - - - ENEMY SECTION - - - - - - - - - - - - - - - - - - - - - - - -


while True:
    move_enemy_ufo()
    
    if is_pressed("shift"):
        fire_bullet()
    
    # screen.mainloop()
    screen.update()
