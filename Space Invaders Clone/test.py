from turtle import Screen, Turtle, register_shape
from winsound import PlaySound, SND_ASYNC
from math import sqrt, pow
from random import randint


border_range = (-300, -300)
border_thickness = 5
player_position = (0, -280)
player_move_distance = 15
number_of_enemies = 5
enemy_move_distance = 2
current_score = 0
missile_move_distance = 20
missile_state = "armed"


# Set up the screen
screen = Screen()
screen.setup(width=650, height=650)
screen.title("Space Invader Alike")
screen.bgpic("space_invaders_background.gif")


# Register the shapes
register_shape("invader.gif")
register_shape("player.gif")


# Draw border
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


def update_scorecard():
    global current_score

    scorestring = f"Score: {current_score}"
    score_card.write(
        scorestring, move=False, align="left", font=("Courier", 14, "normal")
    )


# Draw the current_score
score_card = Turtle()
score_card.speed(0)
score_card.color("white")
score_card.penup()
score_card.setposition(-290, 280)
score_card.hideturtle()
update_scorecard()


# Create the player turtle
player = Turtle()
player.speed(0)
player.penup()
player.color("purple")
player.shape("player.gif")
player.setposition(player_position)
player.setheading(to_angle=90)


enemie_ufos = []
for _ in range(number_of_enemies):  # Add enemies to the list
    enemy_x_position, enemy_y_position = ((randint(-200, 200)), (randint(100, 250)))
    an_enemy_ufo = Turtle()
    an_enemy_ufo.speed(0)
    an_enemy_ufo.penup()
    an_enemy_ufo.shape("invader.gif")
    an_enemy_ufo.setposition(enemy_x_position, enemy_y_position)

    enemie_ufos.append(an_enemy_ufo)


# Create the player's missile
missile = Turtle()
missile.speed(0)
missile.penup()
missile.color("yellow")
missile.shape("triangle")
missile.shapesize(0.5, 0.5)
missile.setheading(to_angle=90)
missile.hideturtle()


# Move the player left and right
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


def fire_missile():
    global missile_state

    if missile_state == "armed":
        PlaySound("laser.wav", SND_ASYNC)
        missile_state = "launch_missile"

        missile_arming_point = ((player.xcor()), (player.ycor() + 10))  # appear just above the player...
        missile.setposition(missile_arming_point)
        missile.showturtle()


def is_colliding(t1, t2):
    distance = sqrt(pow(t1.xcor() - t2.xcor(), 2) + pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


# Create keyboard bindings
screen.listen()
screen.onkeypress(player_moves_left, "Left")
screen.onkeypress(player_moves_right, "Right")
screen.onkey(fire_missile, "space")

# Main game loop
while True:

    for enemy in enemie_ufos:
        # Move the enemy
        x = enemy.xcor()
        x += enemy_move_distance
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 280:
            # Move all enemies down
            for e in enemie_ufos:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemy_move_distance *= -1

        if enemy.xcor() < -280:
            # Move all enemies down
            for e in enemie_ufos:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemy_move_distance *= -1

        # Check for a collision between the missile and the enemy
        if is_colliding(missile, enemy):
            PlaySound("explosion.wav", SND_ASYNC)
            # Reset the missile
            missile.hideturtle()
            missile_state = "armed"
            missile.setposition(0, -400)
            # Reset the enemy
            x = randint(-200, 200)
            y = randint(100, 250)
            enemy.setposition(x, y)
            # Update the current_score
            current_score += 10
            score_card.clear()
            update_scorecard()

        if is_colliding(player, enemy):
            PlaySound("explosion.wav", SND_ASYNC)
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            break

    # Move the missile
    if missile_state == "launch_missile":
        y = missile.ycor()
        y += missile_move_distance
        missile.sety(y)

    # Check to see if the missile has gone to the top
    if missile.ycor() > 275:
        missile.hideturtle()
        missile_state = "armed"
