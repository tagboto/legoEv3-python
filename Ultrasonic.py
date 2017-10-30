#!/usr/bin/env python3
import ev3dev.ev3 as ev3

import library

btn = ev3.Button() 
us = ev3.UltrasonicSensor() 
assert us.connected, "Connect a single US sensor to any sensor port"

# Put the US sensor into distance mode.
us.mode='US-DIST-CM'

units = us.units
# reports 'cm' even though the sensor measures 'mm'

def obstacle():
  while True:  
   if btn.any():
    break
   distance = us.value()/10  # convert mm to cm
   print(distance)
    
   if(distance > 10):
      library.runForever(500)
    
   else:
      library.turnRight(90, 500)
    
      
      
obstacle()
