import math
import turtle as t

def coracaoa (k):
    return 15*math.sin(k)**3
def coracaob(k):
    return 12*math.cos(k)-5*\
    math.cos(2*k)-2*\
    math.cos(3*k)-\
    math.cos(4*k)

t.speed(0)
tela = t.Screen()
t.bgcolor("black")
tela.setup(width=1.0, height=1.0)  # ocupa toda a tela
root = tela.cv._rootwindow
root.attributes("-fullscreen", True)
canvas = tela.getcanvas()
canvas.config(highlightthickness=0, bd=0)  




for i in range (10):   
    t.goto(coracaoa(i)*20,coracaob(i)*20)
    for j in range (5):
        t.color("red")
    t.goto(0,0)
    
t.clear()
t.hideturtle()  
t.penup()
t.goto(0, 0)
t.color("white")
t.write("Fim ❤️", align="center", font=("Arial", 36, "bold"))


t.done()
