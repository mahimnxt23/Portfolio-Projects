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
fire_sound = "sounds/laser.wav"
explosion_sound = "sounds/explosion.wav"


# Set up the screen
screen = Screen()
screen.setup(width=650, height=650)
screen.title("Space Invader Alike")
screen.bgpic("images/space_invaders_background.gif")


# Register the shapes
register_shape("images/invader.gif")
register_shape("images/player.gif")


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
player.shape("images/player.gif")
player.setposition(player_position)
player.setheading(to_angle=90)


def place_an_enemy(obj):
    enemy_x_position, enemy_y_position = ((randint(-200, 200)), (randint(100, 250)))
    obj.setposition(enemy_x_position, enemy_y_position)
    return


enemie_ufos = []
for _ in range(number_of_enemies):  # Add enemies to the list
    an_enemy_ufo = Turtle()
    an_enemy_ufo.speed(0)
    an_enemy_ufo.penup()
    an_enemy_ufo.shape("images/invader.gif")
    place_an_enemy(obj=an_enemy_ufo)

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
        PlaySound(fire_sound, SND_ASYNC)
        missile_state = "launch_missile"

        missile_arming_point = (
            (player.xcor()),
            (player.ycor() + 10),
        )  # appear just above the player...
        missile.setposition(missile_arming_point)
        missile.showturtle()


def is_colliding_between(point1, point2):
    squared_distance_difference_of_x = pow(point1.xcor() - point2.xcor(), 2)
    squared_distance_difference_of_y = pow(point1.ycor() - point2.ycor(), 2)

    position_distance = sqrt(
        squared_distance_difference_of_x + squared_distance_difference_of_y
    )
    if position_distance < 15:
        return True
    else:
        return False


# Create keyboard bindings
screen.listen()
screen.onkeypress(player_moves_left, key="Left")
screen.onkeypress(player_moves_right, key="Right")
screen.onkey(fire_missile, key="space")

# Main game loop
while True:

    for enemy_ufo in enemie_ufos:
        ufo_x_position = enemy_ufo.xcor()
        ufo_x_position += enemy_move_distance
        enemy_ufo.setx(ufo_x_position)

        if (
            ufo_x_position >= 280 or ufo_x_position <= -280
        ):  # Move the enemy back and down

            for ufo in enemie_ufos:
                ufo_y_position = ufo.ycor()
                ufo_y_position -= 20  # Move all enemies down
                ufo.sety(ufo_y_position)

            enemy_move_distance *= -1  # Change enemy direction

        # Check for a collision between the missile and the enemy
        if is_colliding_between(missile, enemy_ufo):
            PlaySound(explosion_sound, SND_ASYNC)
            # Reset the missile
            missile.hideturtle()
            missile_state = "armed"
            missile.setposition(-900, -900)
            # Reset the enemy
            place_an_enemy(obj=enemy_ufo)
            
            # Update the current_score
            current_score += 10
            score_card.clear()
            update_scorecard()

        if is_colliding_between(player, enemy_ufo):
            PlaySound(explosion_sound, SND_ASYNC)
            player.hideturtle()
            enemy_ufo.hideturtle()
            print("Game Over")
            break

    # Move the missile
    if missile_state == "launch_missile":
        missile_y_position = missile.ycor()
        missile_y_position += missile_move_distance
        missile.sety(missile_y_position)

    # Check to see if the missile has gone to the top
        if missile_y_position >= 275:
            missile.hideturtle()
            missile_state = "armed"
