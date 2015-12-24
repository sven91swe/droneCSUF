__author__ = 'Sven'

import support
import threading
import time
import network
import settings

class Control:
    def __init__(self,n):
        self.network=n
        self.controlBehaviors=[0]*3
        self.currentBehavior=0

        self.controlBehaviors[0]=WaypointsCheck(0,self.network,self)
        self.controlBehaviors[1]=None
        self.controlBehaviors[2]=None

        self.controlBehaviors.start()

    def nextBehavior(self,k):

        self.currentBehavior=k+1

        if self.currentBehavior<len(self.controlBehaviors):
            self.controlBehaviors[self.currentBehavior].start()


class Behavior(threading.Thread):
    def __init__(self,k,n,p):
        threading.Thread.__init__(self)

        self.network=n
        self.k=k
        self.parent=p

    def endBehavior(self):
        self.parent.nextBehavior(self.k)


class WaypointsCheck(Behavior):
    def __init__(self,k,n,p):
        super(WaypointsCheck,self).__init__(k,n,p)


        self.waypoints=settings.waypoints
        self.k=0
        self.endK=len(self.waypoints)

        self.points=[0]*self.endK

        for i in range(self.endK):
            w=self.waypoints[i]
            self.points[i]=support.Point(w[1],w[0],w[2])


    def run(self):
        for i in range(self.endK):
            currentState=self.network.getCurrentState()

            print("Going for waypoint number: "+str(i))

            while support.Point.distanceBetweenPoints3D(currentState.point,self.points[i])>40:
                currentState=self.network.getCurrentState()
                time.sleep(0.1)
                print("DistanceToNextWaypoint: "+str(support.Point.distanceBetweenPoints3D(currentState.point,self.points[i])))


        self.endBehavior()

class WaypointGuide(Behavior):
    def __init__(self,k,n,p):
        super(WaypointGuide,self).__init__(k,n,p)


        self.k=0
        self.endK=5

        self.waypoints=[0]*self.endK

        #FlySomewhere
        self.waypoints[0]=support.Point()
        self.waypoints[1]=support.Point()
        self.waypoints[2]=support.Point()
        self.waypoints[3]=support.Point()
        self.waypoints[4]=support.Point()


    def run(self):
        for i in range(self.endK):
            p=self.points[i]
            nextWayPointToPlane=support.Waypoint("WaypointGuide",1,[p.alt,p.lat,p.long],2)
            self.network.setWaypoint
            currentState=self.network.getCurrentState()


            print("Going for waypoint number: "+str(i))

            while support.Point.distanceBetweenPoints3D(currentState.point,self.points[i])>40:
                currentState=self.network.getCurrentState()
                time.sleep(0.1)
                print("DistanceToNextWaypoint: "+str(support.Point.distanceBetweenPoints3D(currentState.point,self.points[i])))


        self.endBehavior()

class Auto(Behavior):
    def run(self):
        self.network.setWaypoint(support.Waypoint("Auto",0,[0,0,0],1))
        self.endBehavior()

class Avoid(Behavior):
    @property
    def nextWaypoint(self):
        currentState=self.network.getCurrentState()
        pos=currentState.getPosition()
        return support.Waypoint("Avoid", 1, pos)

class SimpleTestBehavior(threading.Thread):
    def __init__(self, n):
        threading.Thread.__init__(self)

        self.network=n

        self.wayPoint1=support.Waypoint("SimpleTestBehavior", 0, [50, 38.148188, -76.433375],2)
        self.wayPoint2=support.Waypoint("SimpleTestBehavior", 0, [50, 38.143185, -76.432982],2)
        self.wayPoint3=support.Waypoint("SimpleTestBehavior", 0, [50, 38.147406, -76.426715],2)

        self.start()

    def run(self):
        while True:
            print("WayPoint 1")
            self.network.setWaypoint(self.wayPoint1)
            time.sleep(60)
            print("WayPoint 2")
            self.network.setWaypoint(self.wayPoint2)
            time.sleep(60)
            print("WayPoint 3")
            self.network.setWaypoint(self.wayPoint3)
            time.sleep(60)

