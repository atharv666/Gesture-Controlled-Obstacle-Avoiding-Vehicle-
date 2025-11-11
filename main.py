import sys
sys.path.append('/lib')  

from machine import Pin, I2C, UART
import mpu9250
import time
import math

# ----- I2C Setup -----
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
imu = mpu9250.MPU9250(i2c)

# UART for Bluetooth (HC-05)
bt = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

cmd = 'S'
speed = 0 #Will be Calculating Speed using slope formula
#Max_speed is taken as 255 and Max_angle as 50 degrees 

while True:
    ax, ay, az = imu.acceleration

    # Calculate pitch and roll in degrees
    pitch = math.atan2(ax, math.sqrt(ay**2 + az**2)) * 57.3
    roll  = math.atan2(ay, math.sqrt(ax**2 + az**2)) * 57.3
    
    if pitch < -10:   # forward
        cmd = 'F'
        speed = int(min((51 / 10) * abs(pitch), 255)) #Calculating Speed using slope formula
    elif pitch > 10:  # backward
        cmd = 'B'
        speed = int(min((51 / 10) * abs(pitch), 255))
    elif roll > 10:   # right
        cmd = 'R'
        speed = int(min((51 / 10) * abs(roll), 255))
    elif roll < -10:  # left
        cmd = 'L'
        speed = int(min((51 / 10) * abs(roll), 255))
    else:
        cmd = 'S'
        speed = 0

    # Send command as "F,120" etc.
    message = "{}{:03d}\n".format(cmd, speed)
    bt.write(message)
    print("Pitch: {:.1f}, Roll: {:.1f}, Cmd: {}, Speed: {}".format(pitch, roll, cmd, speed))
    time.sleep(0.2)