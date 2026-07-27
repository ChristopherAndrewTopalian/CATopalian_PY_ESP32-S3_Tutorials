from machine import Pin, ADC, PWM
import time

# SETUP HARDWARE PINS
# Light Sensor on Analog Pin 4 (Configured to read 0V to 3.3V)
light_sensor = ADC(Pin(4))
light_sensor.atten(ADC.ATTN_11DB)

# Servo Motor on Pin 13 (Servos require a 50Hz frequency)
servo = PWM(Pin(13), freq=50)

# WYSIWYG SERVO HELPER FUNCTION
# Translates human angles (0 to 180 degrees) into hardware motor signals
def move_arm(angle):
    # Calculate 16-bit duty cycle (approx 1638 for 0 deg, 8192 for 180 deg)
    duty = int(1638 + (angle / 180) * (8192 - 1638))
    servo.duty_u16(duty)

print("AUTOMATIC SOLAR ROOF / ARM ONLINE")

# STATE MEMORY
# We remember the arm's state so we don't continuously burn out the motor!
arm_is_open = False
move_arm(0)  # Start closed at 0 degrees at boot
print("Status: Nighttime assumed. Arm initialized to CLOSED (0 deg).")

# THE DAY / NIGHT CONTROL LOOP (CORRECTED FOR INVERTED LDR)
while True:
    light_level = light_sensor.read()
    print(f"Sky Lux Reading: {light_level}")

    # MORNING REFLEX: Bright sky now outputs LOW numbers (< 1500)
    if light_level < 1500 and not arm_is_open:
        print(" [!] SUNRISE DETECTED: Opening greenhouse arm to 90 degrees!")
        move_arm(90)     # Swing open!
        arm_is_open = True

    # NIGHT REFLEX: Dark sky now outputs HIGH numbers (> 2000)
    elif light_level > 2000 and arm_is_open:
        print(" [!] SUNSET DETECTED: Closing greenhouse arm to 0 degrees!")
        move_arm(0)   # Swing closed!
        arm_is_open = False

    time.sleep_ms(500)

####

# Dedicated to God the Father
# All Rights Reserved Christopher Andrew Topalian Copyright 2000-2026
# https://github.com/ChristopherAndrewTopalian
# https://github.com/ChristopherTopalian
# https://sites.google.com/view/CollegeOfScripting

