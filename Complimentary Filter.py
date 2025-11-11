# from machine import Pin, I2C, UART
# import mpu9250
# import time
# import math
# 
# # ----- I2C Setup -----
# i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
# imu = mpu9250.MPU9250(i2c)
# 
# pitchG = 0
# rollG = 0
# yaw = 0
# 
# pitchComp = 0
# rollComp = 0
# 
# errorP = 0
# errorR = 0
# 
# tLoop = 0
# 
# 
# last_time = time.ticks_ms()
# 
# # UART for Bluetooth (HC-05)
# bt = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
# 
# while True:
#     ax, ay, az = imu.acceleration
#     
#     current_time = time.ticks_ms()
#     tLoop = time.ticks_diff(current_time, last_time) / 1000
#     last_time = current_time
# 
#     xgyro = -imu.gyro[1]
#     ygyro = imu.gyro[0]
#     zgyro = imu.gyro[2]
#     
#     
#     pitchG += ygyro * tLoop
#     rollG  += xgyro * tLoop
# #     yaw    += zgyro * tLoop
#     
#     pitchA = (math.atan(ax / az) * 360) / (2 * math.pi)
#     rollA  = (math.atan(ay / az) * 360) / (2 * math.pi)
#     
#     pitchComp = pitchA * 0.15 + 0.85 * (pitchComp + ygyro * tLoop) + errorP * 0.0008
#     rollComp = rollA * 0.15 + 0.85 * (rollComp + xgyro * tLoop) + errorR * 0.0008
#     
#     errorP = errorP + (pitchA - pitchComp) * tLoop
#     errorR = errorR + (rollA - rollComp) * tLoop
# 
# 
#     # Calculate pitch and roll in degrees
#     pitch_final = math.atan2(ax, math.sqrt(ay**2 + az**2)) * 57.3
#     roll_final  = math.atan2(ay, math.sqrt(ax**2 + az**2)) * 57.3
# 
# #     print("Pitch: {:.2f}, Roll: {:.2f}".format(pitch, roll))
#     print("Pitch Comp: ", pitchComp, "Roll Comp: ", rollComp, "Pitch: ", pitch_final, "Roll: ", roll_final)
#     
#     time.sleep(0.2)

from machine import Pin, I2C, UART
import mpu9250
import time
import math

# ----- I2C Setup -----
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
imu = mpu9250.MPU9250(i2c)

pitchG = 0
rollG = 0
yaw = 0

pitchComp = 0
rollComp = 0

errorP = 0
errorR = 0

tLoop = 0
last_time = time.ticks_ms()

# UART for Bluetooth (HC-05) — optional
bt = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# ======= Open CSV file for logging =======
# The file will be saved on the Pico’s internal storage.
# After stopping the program, open the file browser in Thonny to find imu_data.csv
log_file = open("imu_data.csv", "w")

# Write CSV header
log_file.write("time_ms,pitchComp,rollComp,pitchRaw,rollRaw\n")

print("Logging started... Press Ctrl+C to stop.")

try:
    while True:
        ax, ay, az = imu.acceleration

        current_time = time.ticks_ms()
        tLoop = time.ticks_diff(current_time, last_time) / 1000
        last_time = current_time

        xgyro = -imu.gyro[1]
        ygyro = imu.gyro[0]
        zgyro = imu.gyro[2]

        pitchG += ygyro * tLoop
        rollG  += xgyro * tLoop

        pitchA = (math.atan(ax / az) * 360) / (2 * math.pi)
        rollA  = (math.atan(ay / az) * 360) / (2 * math.pi)

        pitchComp = pitchA * 0.15 + 0.85 * (pitchComp + ygyro * tLoop) + errorP * 0.0008
        rollComp = rollA * 0.15 + 0.85 * (rollComp + xgyro * tLoop) + errorR * 0.0008

        errorP = errorP + (pitchA - pitchComp) * tLoop
        errorR = errorR + (rollA - rollComp) * tLoop

        # Calculate pitch and roll in degrees
        pitch_final = math.atan2(ax, math.sqrt(ay**2 + az**2)) * 57.3
        roll_final  = math.atan2(ay, math.sqrt(ax**2 + az**2)) * 57.3

        # Print to Thonny (for monitoring)
        print(f"PitchComp: {pitchComp:.3f}, RollComp: {rollComp:.3f}, PitchRaw: {pitch_final:.3f}, RollRaw: {roll_final:.3f}")

        # Save to file (CSV format)
        log_file.write(f"{current_time},{pitchComp:.3f},{rollComp:.3f},{pitch_final:.3f},{roll_final:.3f}\n")

        # Flush to ensure data is written to disk
        log_file.flush()

        time.sleep(0.02)

except KeyboardInterrupt:
    # Graceful exit
    log_file.close()
    print("Logging stopped. File saved as imu_data.csv.")
