from turtle import Screen, Turtle, register_shape
from winsound import PlaySound, SND_ASYNC
from math import sqrt, pow
from random import randint
# from keyboard import is_pressed


border_range = (-300, -300)
border_thickness = 5
player_position = (0, -280)
player_move_distance = 15
number_of_enemies = 5
enemy_move_distance = 2
current_score = 0


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
    score_card.write(scorestring, move=False, align="left", font=("Courier", 14, "normal"))
    

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


enemies = []
for _ in range(number_of_enemies):  # Add enemies to the list
    x, y = ((randint(-200, 200)), (randint(100, 250)))
    an_enemy_ufo = Turtle()
    an_enemy_ufo.speed(0)
    an_enemy_ufo.penup()
    an_enemy_ufo.shape("invader.gif")
    an_enemy_ufo.setposition(x, y)

    enemies.append(an_enemy_ufo)


# Create the player's bullet
bullet = Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 20

# Define bullet state
# ready state means ready to launch
# fire state means bullet is firing
bulletstate = "ready"


# Move the player left and right
def move_left():
    x = player.xcor()
    x -= player_move_distance
    if x < -280:
        x = -280
    player.setx(x)


def move_right():
    x = player.xcor()
    x += player_move_distance
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    # Declare bulletstate as a global if it needs be changed
    global bulletstate
    if bulletstate == "ready":
        PlaySound("laser.wav", SND_ASYNC)
        bulletstate = "fire"
        # Move the bullet to the just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()


def is_colliding(t1, t2):
    distance = sqrt(
        pow(t1.xcor() - t2.xcor(), 2) + pow(t1.ycor() - t2.ycor(), 2)
    )
    if distance < 15:
        return True
    else:
        return False


# Create keyboard bindings
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# Main game loop
while True:

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemy_move_distance
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemy_move_distance *= -1

        if enemy.xcor() < -280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemy_move_distance *= -1

        # Check for a collision between the bullet and the enemy
        if is_colliding(bullet, enemy):
            
            PlaySound("explosion.wav", SND_ASYNC)
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
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

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"
