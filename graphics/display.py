__author__ = 'Sven'

from graphics import *
import time
import threading
import math

class display():
    def __init__(self,longStart,longEnd,latStart,latEnd,x,y,textX, buffer):

        self.longStart=longStart
        self.longEnd=longEnd
        self.latStart=latStart
        self.latEnd=latEnd

        self.buffer=buffer

        self.x=x
        self.y=y
        self.textX=textX

        self.win = GraphWin("Map", x+textX, y, autoflush=False)
        self.win.setBackground("white")

        self.textField=Rectangle(Point(x,0),Point(x+textX,y))
        self.textField.setFill("gray")
        self.textField.draw(self.win)

        self.altidue=Text(Point(x+textX/2,50),"Altitude")
        self.altidue.draw(self.win)

        self.airspeed=Text(Point(x+textX/2,150),"Airspeed")
        self.airspeed.draw(self.win)

        self.mTime=Text(Point(x+textX/2,250),"M-Time: ")
        self.mTime.draw(self.win)

        self.mMessage=Text(Point(x+textX/2,350),"M: ")
        self.mMessage.draw(self.win)

        self.sTime=Text(Point(x+textX/2,450),"S-Time: ")
        self.sTime.draw(self.win)



        self.airplane=0

        self.currentWaypoints=0
        self.currentBorder=0
        self.currentSearch=0


        t=time.clock()
        while True:
            self.checkBuffer()
            self.win.update()
            timetoSleep=max(0.1-(time.clock()-t),0)
            time.sleep(timetoSleep)
            t=time.clock()
            print(timetoSleep)



    def drawLine(self, positions, color, size):
        p=self.convertPositions(positions)

        w=self.win
        c=[0]*(len(p)-1)
        l=[0]*(len(p)-1)

        for i in range(1,len(p)):
            p1=Point(p[i-1][0],p[i-1][1])
            p2=Point(p[i][0],p[i][1])
            c[i-1]=Circle(p2,size)
            c[i-1].setFill(color)
            l[i-1]=Line(p1,p2)
            l[i-1].setFill(color)

            c[i-1].draw(self.win)
            l[i-1].draw(self.win)

        return [c,l]

    def drawBorder(self, positions, color, size):
        p=[[0,0]]*(len(positions)+1)

        for i in range(len(positions)):
            p[i]=positions[i]

        p[len(p)-1][0]=p[0][0]
        p[len(p)-1][1]=p[0][1]

        r=self.drawLine(p,color,size)

        return r

    def convertPositions(self,p):
        ownP=p

        for i in range(len(ownP)):
            ownP[i][0]=round((ownP[i][0]-self.longStart)/(self.longEnd-self.longStart)*self.x)
            ownP[i][1]=round((ownP[i][1]-self.latStart)/(self.latEnd-self.latStart)*self.y)

        return ownP

    def checkBuffer(self):
        if self.buffer.newBorder:
            #print("New Borders")
            if not self.currentBorder==0:
                self.undrawLine(self.currentBorder)

            self.currentBorder=self.drawBorder(self.buffer.border,"blue",3)
            self.buffer.newBorder=False

        if self.buffer.newSearch:
            #print("New Search")
            if not self.currentSearch==0:
                self.undrawLine(self.currentSearch)

            self.currentSearch=self.drawBorder(self.buffer.search,"green",3)
            self.buffer.newSearch=False

        if self.buffer.newWaypoints:
            #print("New Waypoints")
            if not self.currentWaypoints==0:
                self.undrawLine(self.currentWaypoints)

            self.currentWaypoints=self.drawLine(self.buffer.waypoints,"red",5)
            self.buffer.newWaypoints=False

        if self.buffer.newServerTime:
            self.sTime.setText("S-Time: "+self.buffer.serverTime)

            self.buffer.newServerTime=False

        if self.buffer.newServerMessage:
            self.mTime.setText("M-Time: "+self.buffer.messageTime)
            self.mMessage.setText("M: "+self.buffer.message)

            self.buffer.newServerMessage=False

        if self.buffer.newAirplane:
            if not self.airplane==0:
                self.undrawLine(self.airplane)

            self.airplane=self.drawLine(self.buffer.pos,"black",5)
            self.airspeed.setText(self.buffer.velocity)
            self.altidue.setText(self.buffer.altitude)
            self.buffer.newAirplane=False

    def undrawLine(self, o):
        for a in o:
            for b in a:
                b.undraw()


class screenBuffer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.newBorder=True
        self.border=[[0.05,0.05],[0.05,0.95],[0.95,0.95],[0.95,0.05]]

        #self.newSearch=False
        #self.search=0
        self.setSearchArea([[0.3,0.2],[0.5,0.2],[0.5,0.4]])

        self.newWaypoints=True
        self.waypoints=[[0.1,0.1],[0.9,0.9],[0.9,0.8]]

        self.newServerMessage=False
        self.newServerTime=False

        self.message="ServerMessage: K"
        self.serverTime=str(time.clock())
        self.messageTime=str(time.clock())

        self.altitude=0
        self.velocity=0
        self.internalPos=[[0.5,0.5],[0.45,0.45]]
        self.pos=[[0.5,0.5],[0.45,0.45]]

        self.newAirplane=True




        self.start()

    def run(self):
        k=True
        while True:
            for i in range(100):
                #if k:
                    #self.setNoFlyZone([[0.05,0.5],[0.05,0.95],[0.95,0.95],[0.95,0.5]])
                    #self.setWaypoints([[0.1,0.1],[0.9,0.9],[0.9,0.8]])
                #else:
                    #self.setNoFlyZone([[0.05,0.05],[0.05,0.5],[0.95,0.5],[0.95,0.05]])
                    #self.setWaypoints([[0.9,0.1],[0.1,0.9]])

                k=not k
                self.serverMessage(time.clock(),time.clock()+5,"CSUF"+str(time.clock()))

                self.airplane([0.45*math.cos(math.pi/50*i)+0.5,0.45*math.sin(math.pi/50*i)+0.5],i,i)


                time.sleep(0.50)

    def setNoFlyZone(self,positions):
        self.border=positions
        self.newBorder=True

    def setSearchArea(self,positions):
        self.search=positions
        self.newSearch=True

    def setWaypoints(self,positions):
        self.waypoints=positions
        self.newWaypoints=True

    def serverMessage(self,sT,mT,M):
        self.serverTime=str(sT)
        self.newServerTime=True

        if not M==self.message:
            self.message=str(M)
            self.messageTime=str(mT)
            self.newServerMessage=True

    def airplane(self,p,a,v):
        self.internalPos[0]=self.internalPos[1]
        self.internalPos[1]=p

        self.pos[0][0]=self.internalPos[0][0]
        self.pos[0][1]=self.internalPos[0][1]
        self.pos[1][0]=self.internalPos[1][0]
        self.pos[1][1]=self.internalPos[1][1]

        self.altitude=str(a)
        self.velocity=str(v)

        self.newAirplane=True

b=screenBuffer()
a=graphicTest2(0,1,1,0,800,800,400,b)

