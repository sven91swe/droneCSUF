__author__ = 'Sven'

from graphics import *
import time

def main():
    gWidth=1000
    gHeight=800

    win = GraphWin("My Circle", gWidth, gHeight, autoflush=False)
    win.setBackground("white")

    r2 = Rectangle(Point(800,0),Point(1000,800))
    r2.setFill("gray")

    c = Circle(Point(10,10), 3)
    c.setFill("green")
    r2.draw(win)

    points1=[[100,100],[700,100],[700,700],[100,700]]
    border(win,points1,"blue",3)
    points2=[[200,200],[600,200],[600,600],[200,600]]
    border(win,points2,"red",5)

    c.draw(win)


    t=Text(Point(850,20),"Altitude")
    t.draw(win)

    win.update()

    for i in range(0,95):
        c.move(10,10)
        time.sleep(0.2)
        t.setText("Altitude: "+str(i))

        win.update()

    time.sleep(25)
    win.update()

def border(w, p, color, size):
    temp=p

    points=[0]*(len(temp)+1)
    for i in range(len(temp)):
        points[i]=temp[i]

    points[len(points)-1]=temp[0]

    c=[0]*(len(points)-1)
    l=[0]*(len(points)-1)

    for i in range(1,len(points)):
        p1=Point(points[i-1][0],points[i-1][1])
        p2=Point(points[i][0],points[i][1])
        c[i-1]=Circle(p1,size)
        c[i-1].setFill(color)
        l[i-1]=Line(p1,p2)
        l[i-1].setFill(color)

        c[i-1].draw(w)
        l[i-1].draw(w)

main()