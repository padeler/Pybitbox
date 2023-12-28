import serial

import numpy as np
import time

import cv2
import itertools
import datetime


def read(ser):
    print((str(ser.read(ser.in_waiting))))




def send_time(ser, summer_time=False):
    
    t = int(time.time()) - time.timezone
    if summer_time:
        t += time.daylight * 3600
    
    dt = str(t)
    ser.write(bytearray([2, 1]))
    ser.write(bytearray(dt, "ascii"))
    padding = [0] * (16 * 3 - len(dt))
    ser.write(padding)
    ser.flush()
    print(("Time Sent: " + dt))
    print(("Responce: ", ser.readline()))


if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    time.sleep(2)
    print(ser)
    send_time(ser)
    time.sleep(2)
    read(ser)
    ser.close()
