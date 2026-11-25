import turtle

t = turtle.Turtle()
t.color((0.14, 0.53, 0.67))
t.pendown()
for i in range(4):
    t.forward(100)
    t.left(90)

t.penup()
t.goto(x, y)
t.pendown()
t.goto(x, y)
t.penup()

turtle.exitonclick()
