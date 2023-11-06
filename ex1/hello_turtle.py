

import turtle


def draw_petal():
    """The following function Draws the Leaf """
    turtle.forward(30)
    turtle.right(45)
    turtle.forward(30)
    turtle.right(135)
    turtle.forward(30)
    turtle.right(45)
    turtle.forward(30)
    turtle.right(135)


def draw_flower():
    """The following function Draws the flowers using the petal Function"""
    turtle.left(45)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(135)
    turtle.forward(150)


def draw_flower_and_advance():
    """The following function Draws the Flower Garden"""
    draw_flower()
    turtle.up()
    turtle.right(90)
    turtle.forward(150)
    turtle.right(90)
    turtle.forward(150)
    turtle.left(90)
    turtle.down()


def draw_flower_bed():
    """The following function Draws the Flower Garden"""
    turtle.up()
    turtle.left(180)
    turtle.forward(200)
    turtle.down()
    draw_flower_and_advance()
    draw_flower_and_advance()
    draw_flower_and_advance()


if __name__ == "__main__":
    draw_flower_bed()
    turtle.done()
