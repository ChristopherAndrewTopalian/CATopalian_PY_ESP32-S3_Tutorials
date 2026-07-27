from machine import Pin, I2C
import ssd1306
import time

# SETUP THE I2C COMMUNICATION BUS
# For ESP32-S3, use SCL=Pin(9) and SDA=Pin(8)
i2c_bus = I2C(0, scl=Pin(9), sda=Pin(8))

# INITIALIZE THE OLED DISPLAY (128 pixels wide by 64 pixels high)
oled_width = 128
oled_height = 64
screen = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_bus)

print("OLED GRAPHICS ENGINE ONLINE")

# CLEAR THE BUFFER
# 0 turns all pixels OFF (black), 1 turns all pixels ON (white)
screen.fill(0)

# WRITE TEXT TO THE MEMORY BUFFER
# Format: screen.text("String", X_coordinate, Y_coordinate)
# Y=0 is the top line, Y=64 is the very bottom of the screen
screen.text("Hi everyone!", 16, 10)
screen.text("Welcome to our", 8, 30)
screen.text("hardware lab!", 12, 45)

# PUSH TO THE PHYSICAL SCREEN
# Nothing appears on the glass until you call .show()!
screen.show()
print(" -> Display successfully updated!")

####

# Dedicated to God the Father
# All Rights Reserved Christopher Andrew Topalian Copyright 2000-2026
# https://github.com/ChristopherAndrewTopalian
# https://github.com/ChristopherTopalian
# https://sites.google.com/view/CollegeOfScripting

