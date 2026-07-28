from machine import Pin, I2C
import bmp180
import ssd1306
import time

# INITIALIZE THE SHARED I2C DATA HIGHWAY
# Both the barometer (0x77) and OLED (0x3C) share Pin 9 (Clock) and Pin 8 (Data)
i2c_bus = I2C(0, scl=Pin(9), sda=Pin(8))

# ATTACH DEVICES TO THE BUS
weather_sensor = bmp180.BMP180(i2c_bus)
screen = ssd1306.SSD1306_I2C(128, 64, i2c_bus)

# SETUP STORM WARNING LAMP
storm_led = Pin(2, Pin.OUT)

print("FULL ATMOSPHERIC DASHBOARD ONLINE")

while True:
    # READ SENSOR DATA
    temp_c = weather_sensor.temperature
    pressure_hpa = weather_sensor.pressure / 100
    altitude_m = weather_sensor.altitude
    
    # Send backup copy to Serial Console for debugging
    print(f"Temp: {temp_c:.1f}C | Press: {pressure_hpa:.1f} hPa | Alt: {altitude_m:.1f}m")
    
    # PREPARE THE OLED SCREEN
    screen.fill(0)  # Wipe old numbers from buffer
    
    # Stamp formatted strings into display memory
    # Screen is 128px wide by 64px tall; spacing Y by 14px creates clean rows
    screen.text("WEATHER STATION", 4, 0)
    screen.text(f"Temp : {temp_c:.1f} C", 0, 16)
    screen.text(f"Press: {pressure_hpa:.1f} hPa", 0, 30)
    screen.text(f"Alt  : {altitude_m:.1f} m", 0, 44)
    
    # THE DUAL-REFLEX ALARM LOGIC
    # If pressure drops below 1005 hPa, trigger both visual alarms!
    if pressure_hpa < 1005.0:
        storm_led.value(1)               # Ignite Red Pin 2 LED
        screen.text("! STORM ALERT !", 4, 56) # Print warning on bottom row
        print(" [!] LOW PRESSURE FRONT: STORM INCOMING [!]")
    else:
        storm_led.value(0)               # Stand down LED
        screen.text("Status: Normal", 0, 56)
        
    # BLAST BUFFER TO PHYSICAL GLASS
    screen.show()
    
    # Update dashboard every 1.5 seconds
    time.sleep_ms(1500)

####

# Dedicated to God the Father
# All Rights Reserved Christopher Andrew Topalian Copyright 2000-2026
# https://github.com/ChristopherAndrewTopalian
# https://github.com/ChristopherTopalian
# https://sites.google.com/view/CollegeOfScripting

