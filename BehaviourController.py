#!/usr/bin/env python3
#Writen by Zoe Tagboto, Benedict Quartey and Brenda Mboya

import ev3dev.ev3 as ev3
import library
from time import sleep

#We used this to implement threading 
from threading import Thread

#Importing the various sensors used by our robot
camera = ev3.Sensor(address=ev3.INPUT_4) #Importing the pixycam
btn = ev3.Button() #Importing the button which was used to start and stop the program
us = ev3.UltrasonicSensor() #importing the ultrasonc sensor to measure distance

assert us.connected, "Connect a single US sensor to any sensor port"
assert camera.connected,  "Error while connecting Pixy camera to port 4"

# Put the US sensor into distance mode.
us.mode='US-DIST-CM'
units = us.units # reports 'cm' even though the sensor measures 'mm'

#The pixels in the camera
CAMERA_WIDTH_PIXELS = 255
CAMERA_HEIGHT_PIXELS = 255


#These are the threads we declare them globally so we can end the threads easily
global wander
global approach
global avoid

#Because with threading we couldn't reference sensors in multiple sensors we made global variables. 
global distance
global x,y,w,h
global objCount

# We made wander and avoid our main functions so they are the default actions or robot takes 
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


# This function is what we call the avoid thread. It avoids an obstacle that is not green and moves
# a certain distance away.
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
               #If the object is green or the distance is not less than D it turns off
                #this thread and switches on approach
                wander = False
                approach=True

def setCameraMode(): #This sets the camera to look for green
    camera.mode = 'SIG1'

#This function approaches a green object and stops a certain distance away.
def approachObj():
    global approach
    global wander
    while (not btn.any()):
        if approach==True:
            if objCount > 0: #If there is more than one green object seen by the pixycam
                if(x < CAMERA_WIDTH_PIXELS/2 - w/2): #Checks if object is to the left of camera
                    print("  Object is to my left.")
                    library.stopMotors()
                    library.turning(0,200)

                elif (x > CAMERA_WIDTH_PIXELS/2 + w/2): #Checks if the object is to the right of the camera
                    print("  Object is to my right.")
                    library.stopMotors()
                    library.turning(200,0)

                else:
                    if(distance>D): #If the object is too far away the robot drives towards it
                        library.stopMotors()
                        library.runForever(200)
                    else:
                        print("  Object is approximately in front of me.") 
                        ev3.Sound.beep() #Beeps when the object is the specified distance and beeps.
                        library.stopMotors()
                        sleep(5)
                    
            else:# If a green object not found it stops this thread and runs wander
                wander=True
                approach = False
                
                
  

def wanderTillCenter(): #This functionn wanders till a green object is found
    global approach
    global wander
    global distance
  
    while (not btn.any()):
        if wander == True :
            if objCount > 0: # Checks If a green object is found
                print("Found a green object") 
                ev3.Sound.beep()
                library.stopMotors()
                approach =True
                wander = False
                
            
            elif objCount==0: #If not found, turns until it is found
              library.turning(500,0)

        
#This was done to chnage our individual functions to threads.           
wanderThread =  Thread(target=wanderTillCenter)
wanderThread.start()
approachThread =  Thread(target=approachObj)  
approachThread.start()
avoidThread = Thread(target=avoidObstacle)
avoidThread.start()

#This is our main function 
def main():
    global wander
    global approach
    global avoid
    global distance
    global x,y,w,h
    global objCount
    
    print("Looking for green......")
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
