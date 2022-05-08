import turtle
from math import *
vert_asymp_list=[]
horiz_asymp_list=[]
#(sin(x**3+3)-4)*(x-1)
def safe_math_eval(stringfunc, x, gap):
    rel_xval = x/gap
    rel_xval = str("("+str(rel_xval)+")")
    global vert_asymp_list
    global horiz_asymp_list
    skipflag=0
    stringfunc = stringfunc.replace("x", str(rel_xval))
    allowed_chars = "0123456789+-*(). /^"
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
            print(i)
            raise Exception("Unsafe eval")
            
            
    try:
        return(eval(stringfunc))
        #horizcheck:
        inverse_stringfunc = stringfunc.swap
            
        
    except:
        vert_asymp_list.append(x)
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
def drawasymp(vert, horiz, scale):
    #vert:
    turtle.pencolor("green")
    for i in range(0, len(vert)):
        turtle.pu()
        turtle.goto(vert[i], scale)
        turtle.pd()
        turtle.goto(vert[i], -scale)
    turtle.pencolor("black")
    #horiz:
##    for i in range(0, len(horiz)):
##        turtle.pu()
##        turtle.goto(-scale, vert[i])
##        turtle.pd()
##        turtle.goto(scale, vert[i])
        
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
for xval in range(-halfsize, halfsize):
    turtle.pd()
    #rel_xval = xval/gap
    #rel_xval = str("("+str(rel_xval)+")")
    #print(rel_xval)
    #print(safe_math_eval(func, rel_xval))
    turtle.goto(xval, (safe_math_eval(func, xval, gap))*gap)
    #turtle.goto(xval, (safe_math_eval(func, rel_xval, gap))*gap)
    turtle.pu()
drawasymp(vert_asymp_list, horiz_asymp_list, scale)
