from machine import Pin, time_pulse_us
import time

# Define Hardware Pins (WYSIWYG Direct Mapping)
trig_pin = Pin(4, Pin.OUT)
echo_pin = Pin(5, Pin.IN)
alarm_led = Pin(2, Pin.OUT)

print("TACTICAL RADAR SYSTEM ONLINE (MICROPYTHON)")

# The Infinite Proximity Loop
while True:
    # Ensure the trigger pin is quiet before firing
    trig_pin.value(0)
    time.sleep_us(2)

    # Fire the 10-microsecond high-voltage ultrasonic sound pulse
    trig_pin.value(1)
    time.sleep_us(10)
    trig_pin.value(0)

    # Measure echo time: listens for ECHO pin to go HIGH (1) with a 30,000us max timeout (~5 meters)
    duration = time_pulse_us(echo_pin, 1, 30000)

    # Calculate distance and evaluate perimeter security
    if duration > 0:
        # Speed of sound is ~0.0343 cm per microsecond. Divide by 2 for round-trip!
        distance_cm = (duration * 0.0343) / 2
        print(f"Target Range: {distance_cm:.1f} cm")
        
        # Trigger alarm if object breaches the 50cm perimeter
        if distance_cm < 50:
            alarm_led.value(1)  # Fire warning LED
            print(" [!] PERIMETER BREACH DETECTED [!]")
        else:
            alarm_led.value(0)  # Stand down
    else:
        print("Target out of range or sensor timeout")
        alarm_led.value(0)
        
    # Wait 100 milliseconds before sending the next radar ping (10 Hz loop)
    time.sleep_ms(100)

####

# Dedicated to God the Father
# All Rights Reserved Christopher Andrew Topalian Copyright 2000-2026
# https://github.com/ChristopherAndrewTopalian
# https://github.com/ChristopherTopalian
# https://sites.google.com/view/CollegeOfScripting

