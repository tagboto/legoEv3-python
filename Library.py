#!/usr/bin/env python3
#Written by Zoe Tagboto, Brenda Mboya and Benedict Quartey
import ev3dev.ev3 as ev3
import  math

#Creating the variables for the right and a left motor
rightMotor = ev3.LargeMotor('outC')
leftMotor = ev3.LargeMotor('outB')

#function to go forward a specified distance in cm and a given speed
def moveForward(distance, speed):
  encoder=(distance/(2*math.pi*2.8))*360
  rightMotor.run_to_rel_pos(position_sp=encoder, speed_sp=speed,stop_action="brake")
  leftMotor.run_to_rel_pos(position_sp=encoder, speed_sp=speed,stop_action="brake")
  rightMotor.wait_while('running')
  leftMotor.wait_while('running')

#function to turn left a given angle in degrees and a given speed 
def turnLeft(angle, speed): 
  encoder= (angle*13.5)/2.8
  leftMotor.stop()
  rightMotor.run_to_rel_pos(position_sp=encoder, speed_sp=speed,stop_action="brake")
  rightMotor.wait_while('running')
  
#function to turn right a given angle in degrees and a given speed
def turnRight(angle, speed): 
  encoder= (angle*13.5)/2.8
  rightMotor.stop()
  leftMotor.run_to_rel_pos(position_sp=encoder, speed_sp=speed,stop_action="brake")
  leftMotor.wait_while('running')
  

#method to spin the robot right a given angle in degrees and a given speed
def spinRight(angle,speed):
 encoder= (angle*13.5)/2.8
 rightMotor.run_to_rel_pos(position_sp=-encoder, speed_sp=speed,stop_action="brake")
 leftMotor.run_to_rel_pos(position_sp=encoder, speed_sp=speed,stop_action="brake")
 rightMotor.wait_while('running')
 leftMotor.wait_while('running')

#method to spin the robot left a given angle in degrees and a given speed
def spinLeft(angle,speed):
 encoder= (angle*13.5)/2.8
 rightMotor.run_to_rel_pos(position_sp=encoder, speed_sp=speed,stop_action="brake")
 leftMotor.run_to_rel_pos(position_sp=-encoder, speed_sp=speed,stop_action="brake")
 rightMotor.wait_while('running')
 leftMotor.wait_while('running')



