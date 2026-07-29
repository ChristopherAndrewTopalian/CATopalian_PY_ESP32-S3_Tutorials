from machine import Pin, PWM
import time

# Initialize PWM on Pin 13 at 50Hz (Standard for all servos)
servo = PWM(Pin(13), freq=50)

# Define our mechanical limits 
# (MicroPython uses a 16-bit resolution, so values range from 0 to 65535)
# Note: If your servo aggressively buzzes at these limits, it is hitting its 
# physical plastic stops. Adjust these numbers inward (e.g., 3000 and 7000) to protect the gears.
POSITION_CLOSED = 2500  # Roughly 0 degrees
POSITION_OPEN = 7500    # Roughly 180 degrees

print("SERVO SNAP SEQUENCE ONLINE")

while True:
    # Snap to Open
    servo.duty_u16(POSITION_OPEN)
    time.sleep(1)
    
    # Snap to Closed
    servo.duty_u16(POSITION_CLOSED)
    time.sleep(1)

####

# Dedicated to God the Father
# All Rights Reserved Christopher Andrew Topalian Copyright 2000-2026
# https://github.com/ChristopherAndrewTopalian
# https://github.com/ChristopherTopalian
# https://sites.google.com/view/CollegeOfScripting

