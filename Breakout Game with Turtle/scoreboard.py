from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.penup()
        self.hideturtle()
        self.hit_score = 0
        self.remaining_lives = 3
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-100, 300)
        self.write(self.hit_score, align='center', font=('verdana', 25, 'normal'))
        self.goto(100, 300)
        self.write(self.remaining_lives, align='center', font=('verdana', 25, 'normal'))

    def add_score(self):
        self.hit_score += 15
        self.update_scoreboard()

    def deduct_lives(self):
        self.remaining_lives -= 1
        self.update_scoreboard()

    def show_game_over(self):
        self.goto(0, -150)
        self.write('Game over!', align='center', font=('verdana', 30, 'normal'))

    def show_congrats(self):
        self.goto(0, -150)
        self.write('Congratulations 🎉!', align='center', font=('verdana', 30, 'normal'))
