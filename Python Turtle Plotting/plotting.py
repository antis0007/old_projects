import turtle
from math import *
#(sin(x**3+3)-4)*(x-1)
print("Use python math syntax for special evaluation, eg. log(base, x) or sin(x)")
print("Multiplication is NOT implied by brackets, use *")
def safe_math_eval(stringfunc, x):    
    skipflag=0
    stringfunc = stringfunc.replace("x", str(x))
    allowed_chars = "0123456789+-*(). /^,"
    for i in range(0, len(stringfunc)):
        if skipflag>0:
            skipflag=skipflag-1
            continue
        if stringfunc[i] not in allowed_chars:
            #sin check:
            if stringfunc.find("sin") == i:
                skipflag+=len("sin")
                continue
            #cos check:
            if stringfunc.find("cos") == i:
                skipflag+=len("cos")
                continue
            #tan check:
            if stringfunc.find("tan") == i:
                skipflag+=len("tan")
                continue
            #sqrt check:
            if stringfunc.find("sqrt") == i:
                skipflag+=len("sqrt")
                continue
            #log check:
            if stringfunc.find("log") == i:
                skipflag+=len("log")
                continue
            print(i)
            raise Exception("Unsafe eval") 
    try:
        return(eval(stringfunc))            
    except:
        turtle.pu()
        return -100000    

#turtle graphing calculator
size = int(input("Gimme yo screen size: "))
halfsize = int(size/2)
scale = int(input("Gimme the scale of the grid (#squares from origin to edge of axis on any side): "))
halfscale=int(scale/2)
func = str(input("Gimme string for function:"))
#By default samples x vals at resolution of screen

gap = halfsize/scale
screen = turtle.Screen()
screen.setup(size,size)
screen.screensize(size,size)
turtle = turtle.Turtle()
turtle.pu()
turtle.speed(0)#Disable animation, max speed

def drawgrid(scale, halfsize, gap):
    turtle.goto(-halfsize, -halfsize) #bottom left start
    for i in range(0, 2*scale):#Vertical
        turtle.goto(-size/2, (turtle.ycor()+gap))
        turtle.pd()
        turtle.goto(size/2, turtle.ycor())
        turtle.pu()
    turtle.goto(-halfsize, -halfsize)
    for i in range(0, 2*scale):#Horiz
        turtle.goto((turtle.xcor()+gap),-size/2)
        turtle.pd()
        turtle.goto(turtle.xcor(),size/2)
        turtle.pu()
def drawaxis(size):
    turtle.pencolor("red")
    turtle.pu()
    
    turtle.goto(0, -size/2)#Vertical
    turtle.pd()
    turtle.goto(0, size/2)
    turtle.pu()
    turtle.goto(-size/2, 0)#Vertical
    turtle.pd()
    turtle.goto(size/2, 0)
    turtle.pencolor("black")
    turtle.pu()

drawgrid(scale, halfsize, gap)
drawaxis(size)
turtle.pu()
turtle.pencolor("blue")
turtle.goto(-size/2, 0)
#Draw graph loop:
for xval in range(-halfsize, halfsize):
    turtle.pd()
    rel_xval = xval/gap
    rel_xval = str("("+str(rel_xval)+")")
    #print(rel_xval)
    #print(safe_math_eval(func, rel_xval))
    #turtle.goto(xval, (safe_math_eval(func, xval))*gap)
    turtle.goto(xval, (safe_math_eval(func, rel_xval))*gap)
    turtle.pu()

