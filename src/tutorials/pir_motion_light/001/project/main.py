from machine import Pin
import time

# SETUP HARDWARE PINS (Pure WYSIWYG Digital Mapping)
# PIR Sensor on Pin 14 configured to listen for high/low voltages
pir_sensor = Pin(14, Pin.IN)

# Security Floodlight LED on Pin 2 configured to send voltage out
floodlight = Pin(2, Pin.OUT)

print("TACTICAL INFRARED DEFENSE SYSTEM ONLINE")
print("Status: Scanning perimeter for moving heat signatures...")

# Ensure floodlight is OFF at boot
floodlight.value(0)

# THE MAIN PERIMETER SCANNING LOOP
while True:
    # Read the digital pin (Returns exactly 1 or 0)
    motion_detected = pir_sensor.value()

    # REFLEX: If the sensor voltage goes HIGH (1), someone is moving!
    if motion_detected == 1:
        print(" [!] ALARM: Heat signature detected! Engaging floodlight!")
        floodlight.value(1)  # Turn floodlight ON

        # Keep the area illuminated for 3 seconds so we can see the intruder
        time.sleep(3)

        print(" -> Perimeter clear. Shutting down floodlight.")
        floodlight.value(0)  # Turn floodlight OFF

    # Check the sensor 10 times every second (100 milliseconds)
    time.sleep_ms(100)

####

# Dedicated to God the Father
# All Rights Reserved Christopher Andrew Topalian Copyright 2000-2026
# https://github.com/ChristopherAndrewTopalian
# https://github.com/ChristopherTopalian
# https://sites.google.com/view/CollegeOfScripting

