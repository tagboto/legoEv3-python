#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import library
from time import sleep
from threading import Thread

camera = ev3.Sensor(address=ev3.INPUT_4)
btn = ev3.Button() 
us = ev3.UltrasonicSensor() 
assert us.connected, "Connect a single US sensor to any sensor port"
assert camera.connected,  "Error while connecting Pixy camera to port 4"

# Put the US sensor into distance mode.
us.mode='US-DIST-CM'

CAMERA_WIDTH_PIXELS = 255
CAMERA_HEIGHT_PIXELS = 255
units = us.units # reports 'cm' even though the sensor measures 'mm'


global wander
global approach
global avoid
global distance
global x,y,w,h
global objCount


wander = True
approach = False
avoid = True


sigNum = 1
D= 15
distance = us.value()/10
x = camera.value(1)
y = camera.value(2)
w = camera.value(3)
h = camera.value(4)
objCount = camera.value(0)



def avoidObstacle():
    global avoid
    global approach
    global distance

    
    while (not btn.any()):
        if avoid ==True:
            if(distance<D and objCount==0):
                print("There is an object in my path")
                library.moveForward(-7,200)
                library.turnRight(90,200)
                library.moveForward(20,200)
            else:
                wander = False
                approach=True

def setCameraMode():
    camera.mode = 'SIG1'

def approachObj():
    global approach
    global wander
    while (not btn.any()):
        if approach==True:
            if objCount > 0:
                if(x < CAMERA_WIDTH_PIXELS/2 - w/2):
                    print("  Object is to my left.")
                    library.stopMotors()
                    library.turning(0,200)

                elif (x > CAMERA_WIDTH_PIXELS/2 + w/2): #Checks if the object is to the right of the camera
                    print("  Object is to my right.")
                    library.stopMotors()
                    library.turning(200,0)

                else:
                    if(distance>D):
                        library.stopMotors()
                        library.runForever(200)
                    else:
                        print("  Object is approximately in front of me.") #Checks if the object is infront of the camera
                        ev3.Sound.beep()
                        library.stopMotors()
                        sleep(5)
                    
            else:
                wander=True
                approach = False
                
                
  

def wanderTillCenter():
    global approach
    global wander
    global distance
  
    while (not btn.any()):
        if wander == True :
            if objCount > 0: 
                print("Now going to approach object") #Checks if the object is infront of the camera
                ev3.Sound.beep()
                library.stopMotors()
                approach =True
                wander = False
                
            
            elif objCount==0:
              library.turning(500,0)

        
            
wanderThread =  Thread(target=wanderTillCenter)
wanderThread.start()
approachThread =  Thread(target=approachObj)  
approachThread.start()
avoidThread = Thread(target=avoidObstacle)
avoidThread.start()


def main():
    global wander
    global approach
    global avoid
    global distance
    global x,y,w,h
    global objCount
    
    print("Hi")
    setCameraMode()
    while (not btn.any()):
    
        distance = us.value()/10
        x = camera.value(1)
        y = camera.value(2)
        w = camera.value(3)
        h = camera.value(4)
        objCount = camera.value(0)
        
        
        if wander ==True:
            approach =False
            
        elif approach ==True:
            wander =False

    library.stopMotors()
     
main()
