from machine import Pin, ADC
import time

# ==================
# HARDWARE PIN SETUP
# Direction (DIR) and Step (STEP) control pins for the A4988 driver
dir_pin = Pin(16, Pin.OUT)
step_pin = Pin(17, Pin.OUT)

# Analog Joystick Vertical (Y-Axis) connected to Pin 4
joystick_y = ADC(Pin(4))
joystick_y.atten(ADC.ATTN_11DB)  # Configures pin to read full 0V - 3.3V range

# ==================
# TUNING PARAMETERS
# ==================
# Joystick resting deadzone thresholds (0 to 65535 scale)
LOWER_DEADZONE = 20000
UPPER_DEADZONE = 45000

# Speed delay in microseconds (Lower = Faster, Higher = Slower)
STEP_DELAY_US = 1000  

print("ROBOTIC ARM STEPPER SYSTEM READY")

# ==================
# CONTROL LOOP
# ==================
while True:
    # Read the physical analog position of the joystick (0 to 65535)
    y_val = joystick_y.read_u16()
    
    # Joystick pushed DOWN: Counterclockwise Rotation
    if y_val < LOWER_DEADZONE:
        dir_pin.value(0)           # Set direction signal to LOW
        step_pin.value(1)          # Pulse STEP High
        time.sleep_us(STEP_DELAY_US)
        step_pin.value(0)          # Pulse STEP Low
        time.sleep_us(STEP_DELAY_US)
        
    # Joystick pushed UP: Clockwise Rotation
    elif y_val > UPPER_DEADZONE:
        dir_pin.value(1)           # Set direction signal to HIGH
        step_pin.value(1)          # Pulse STEP High
        time.sleep_us(STEP_DELAY_US)
        step_pin.value(0)          # Pulse STEP Low
        time.sleep_us(STEP_DELAY_US)
        
    # Joystick at REST: Do nothing
    else:
        pass

####

# Dedicated to God the Father
# All Rights Reserved Christopher Andrew Topalian Copyright 2000-2026
# https://github.com/ChristopherAndrewTopalian
# https://github.com/ChristopherTopalian
# https://sites.google.com/view/CollegeOfScripting

