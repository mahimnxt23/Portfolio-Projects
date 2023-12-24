from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.penup()
        self.hideturtle()
        self.hit_score = 0
        self.remaining_lives = 5
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-100, 300)
        self.write(self.hit_score, align='center', font=('courier', 25, 'normal'))
        self.goto(100, 300)
        self.write(self.remaining_lives, align='center', font=('courier', 25, 'normal'))

    def left_point(self):
        self.hit_score += 15
        self.update_scoreboard()

    def right_point(self):
        self.remaining_lives -= 1
        self.update_scoreboard()
