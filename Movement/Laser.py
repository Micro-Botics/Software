from machine import Pin, I2C
from vl53l5cx import VL53L5CX
import time

# ESP32 default I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

sensor = VL53L5CX(i2c)

print("Initializing sensor...")
sensor.init()

# Choose resolution: 16 (4×4) or 64 (8×8)
sensor.resolution = 64

# Range frequency in Hz (1–15)
sensor.ranging_frequency = 10

# Start measurement
sensor.start()

while True:
    if sensor.data_ready:
        frame = sensor.read()

        # frame.distance_mm → list of 64 integers
        distances = frame.distance_mm

        # Pretty print 8×8 grid
        for r in range(8):
            print(distances[r*8:(r+1)*8])
        print()
    
    time.sleep(0.01)
