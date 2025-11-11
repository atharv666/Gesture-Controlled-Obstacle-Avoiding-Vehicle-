# from machine import Pin, I2C, UART
# import mpu9250
# import time
# import math
# 
# i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
# imu = mpu9250.MPU9250(i2c)
# 
# confValue = 0.1
# pitch = 0
# roll = 0
# 
# # UART for Bluetooth (HC-05)
# bt = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
# 
# while True:
#     ax, ay, az = imu.acceleration
#     
#     #   Low Pass Filter applied to bith pitch and roll
#     pitch = confValue * math.atan(ax / az) + (1 - confValue) * pitch
#     pitch_degrees = (pitch * 360) / (2 * math.pi)
#     
#     roll = confValue * math.atan(ay / az) + (1 - confValue) * roll
#     roll_degrees = (roll * 360) / (2 * math.pi)
# 
# 
#     # Calculate pitch and roll in degrees
#     pitch_final = math.atan2(ax, math.sqrt(ay**2 + az**2)) * 57.3
#     roll_final  = math.atan2(ay, math.sqrt(ax**2 + az**2)) * 57.3
# 
# #     print("Pitch: {:.2f}, Roll: {:.2f}".format(pitch, roll))
#     print("Pitch Low Pass: ", pitch_degrees, "Roll Low Pass: ", roll_degrees, "Pitch: ", pitch_final, "Roll: ", roll_final)
#     
#     time.sleep(0.2)

from machine import Pin, I2C, UART
import mpu9250
import time
import math

# ----- I2C Setup -----
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
imu = mpu9250.MPU9250(i2c)

confValue = 0.1
pitch = 0
roll = 0

# UART for Bluetooth (HC-05)
bt = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# ----- File Setup -----
filename = "imu_lpf.csv"
with open(filename, "w") as f:
    f.write("time_ms,pitchLPF,rollLPF,pitchRaw,rollRaw,time_s\n")

start_time = time.ticks_ms()

while True:
    ax, ay, az = imu.acceleration

    # Low-Pass Filter applied to both pitch and roll
    pitch = confValue * math.atan(ax / az) + (1 - confValue) * pitch
    pitch_degrees = (pitch * 360) / (2 * math.pi)

    roll = confValue * math.atan(ay / az) + (1 - confValue) * roll
    roll_degrees = (roll * 360) / (2 * math.pi)

    # Raw pitch and roll
    pitch_final = math.atan2(ax, math.sqrt(ay**2 + az**2)) * 57.3
    roll_final  = math.atan2(ay, math.sqrt(ax**2 + az**2)) * 57.3

    # Timing
    t_ms = time.ticks_diff(time.ticks_ms(), start_time)
    t_s = t_ms / 1000.0

    # Save data to CSV
    with open(filename, "a") as f:
        f.write(f"{t_ms},{pitch_degrees:.2f},{roll_degrees:.2f},{pitch_final:.2f},{roll_final:.2f},{t_s:.3f}\n")

    print("Pitch Low Pass:", pitch_degrees, "Roll Low Pass:", roll_degrees,
          "Pitch Raw:", pitch_final, "Roll Raw:", roll_final)

    time.sleep(0.2)
