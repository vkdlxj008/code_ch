from turtle import Turtle

SPACING = 0.75

class Draw(Turtle):
    def __init__(self):
        super().__init__()


    def draw_board(self):
        '''
            Draws a 3x3 grid board using the turtle graphics library.

            This function sets the pen color to white and pen size to 10, then
            draws two horizontal lines and two vertical lines to form a 3x3 grid.

            Specifically:
        - Horizontal lines are drawn at y-coordinates -1 and 1.
        - Vertical lines are drawn at x-coordinates -1 and 1.
        '''

        self.pencolor('white')
        self.pensize(10)
        self.hideturtle()

        for y in [-1, 1]:
            self.up()
            self.goto(-3, y)
            self.seth(0)
            self.down()
            self.fd(6)

        for x in [-1, 1]:
            self.up()
            self.goto(x, -3)
            self.seth(90)
            self.down()
            self.fd(6)

    def draw_circle(self, row, col):
        x = (col - 1) * 2
        y = (1 - row) * 2
        self.up()
        self.goto(x, y - SPACING)
        self.seth(0)
        self.color("red")
        self.down()
        self.circle(SPACING, steps=100)

    def draw_x(self, row, col):
        x = (col - 1) * 2
        y = (1 - row) * 2
        self.color('blue')
        self.up()
        self.goto(x - SPACING, y - SPACING)
        self.down()
        self.goto(x + SPACING, y + SPACING)
        self.up()
        self.goto(x - SPACING, y + SPACING)
        self.down()
        self.goto(x + SPACING, y - SPACING)