import serial

import numpy as np
import time

import cv2
import itertools
import datetime


def read(ser):
    print((str(ser.read(ser.in_waiting))))


def send_image(ser, bgr):
    buf = bgr[:, :, ::-1].flatten().tolist()
    ser.write(bytearray([10, 16]))
    ser.write(buf)


def send_settings(ser, clock_mode=0, brightness=20):

    set = " %d %d" % (clock_mode, brightness)
    ser.write(bytearray([1, 1]))

    print(("SENDING: [%s]" % set))
    ser.write(set)
    print(("Responce: ", ser.readline()))


def send_time(ser):

    dt = str(int(time.time()) - time.timezone)# + time.daylight * 3600)
    ser.write(bytearray([2, 1]))
    ser.write(bytearray(dt, "ascii"))
    padding = [0] * (16 * 3 - len(dt))
    ser.write(padding)
    ser.flush()
    print(("Time Sent: " + dt))
    print(("Responce: ", ser.readline()))


def run(ser):
    imgs = []
    img = cv2.imread("res/mario.jpg")
    img = cv2.imread("res/minnie2.png")
    img = cv2.imread("res/mickey.png")
    imgs.append(cv2.imread("res/frog.png"))
    imgs.append(img)
    # test = np.zeros((16,16,3), dtype=np.ubyte)
    # test[:, :] = [200,200,200]
    # imgs.append(test)

    image_filenames = [
        # "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/0.bmp",
        # "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/1.bmp",
        # "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/2.bmp",
        # "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/3.bmp",
        # "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/4.bmp",
        # "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/5.bmp",
        # "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/6.bmp",
        # "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/7.bmp",
        # "/home/padeler/work/PixelFrame/art/heart-Pixel-Chest/heart/8.bmp",
        # "/home/padeler/work/RibbaPi/resources/animations/art/speeder/speeder/0.bmp",
        # "/home/padeler/work/RibbaPi/resources/animations/art/speeder/speeder/1.bmp",
        # "/home/padeler/work/RibbaPi/resources/animations/art/speeder/speeder/2.bmp",
    ]
    # for i in image_filenames:
    # imgs.append(cv2.imread(i))

    frames = itertools.cycle(imgs)
    k = 0
    sleep_time = 1000
    for f in frames:

        bf = cv2.resize(f, (160, 160), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("IMG", bf)

        send_image(ser, f)
        # time.sleep(1)
        # read(ser)

        t = time.time()
        k = cv2.waitKey(sleep_time)
        if k & 0xFF == ord("q"):
            break

        dt = time.time() - t
        print(("DT: ", dt))
        # time.sleep(max(0, 1.0-dt))

    time.sleep(2)
    img = np.zeros((16, 16, 3), dtype=np.ubyte)
    send_image(ser, img)
    time.sleep(1)
    read(ser)


def test(ser):

    ser.write(bytearray([10, 2, 0, 0, 0, 0, 0, 0]))
    time.sleep(2)
    read(ser)
    time.sleep(2)


if __name__ == "__main__":
    # ser = serial.Serial("/dev/ttyUSB0", 115200, dsrdtr=True)
    # ser = serial.Serial("/dev/ttyUSB0", 115200)
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    time.sleep(2)
    print(ser)
    send_time(ser)
    # test(ser)
    time.sleep(2)
    # read(ser)
    # send_settings(ser, 2, 30)
    # run(ser)

    # time.sleep(1)
    read(ser)
    ser.close()
