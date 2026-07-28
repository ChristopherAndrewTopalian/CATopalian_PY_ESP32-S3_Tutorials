from machine import Pin, I2C
import bmp180
import time

# SETUP I2C BUS & SENSOR (ESP32-S3 uses SCL=9, SDA=8)
i2c_bus = I2C(0, scl=Pin(9), sda=Pin(8))
weather_sensor = bmp180.BMP180(i2c_bus)

# SETUP STORM WARNING LED
storm_led = Pin(2, Pin.OUT)

print("ATMOSPHERIC SENSOR SUITE ONLINE")
print("Calibrating baseline barometer readings...")

# Baseline sea-level pressure in hectopascals (hPa)
SEA_LEVEL_PRESSURE = 1013.25

while True:
    # Read raw data from the chip
    temp_c = weather_sensor.temperature
    # BMP180 reports pressure in Pascals (Pa), divide by 100 for standard hPa / mbar
    pressure_hpa = weather_sensor.pressure / 100
    
    # Calculate approximate altitude in meters using standard atmospheric formula
    #altitude_m = 44330 * (1 - (pressure_hpa / SEA_LEVEL_PRESSURE) ** (1 / 5.255))
    altitude_m = weather_sensor.altitude
    
    # PRINT FORMATTED TELEMETRY TO THE SERIAL MONITOR
    print(f"Temp: {temp_c:.1f}°C | Pressure: {pressure_hpa:.1f} hPa | Alt: {altitude_m:.1f} m")
    
    # THE REAL-WORLD REFLEX: LOW PRESSURE STORM WARNING
    # If atmospheric pressure drops below 1005 hPa, a storm front is approaching!
    if pressure_hpa < 1005.0:
        print(" [!] WARNING: LOW PRESSURE FRONT DETECTED - STORM INCOMING!")
        storm_led.value(1) # Ignite the Red Storm Alert Lamp
    else:
        storm_led.value(0) # Clear skies / Normal pressure

    time.sleep(2)

####

# Dedicated to God the Father
# All Rights Reserved Christopher Andrew Topalian Copyright 2000-2026
# https://github.com/ChristopherAndrewTopalian
# https://github.com/ChristopherTopalian
# https://sites.google.com/view/CollegeOfScripting

