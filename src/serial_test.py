import serial
import numpy as np
import time
import cv2
import itertools
import datetime

def read(ser):
    print str(ser.read(ser.in_waiting))


def send_image(ser, bgr):
    buf = bgr[:, :, ::-1].flatten().tolist()
    ser.write(bytearray([10, 16]))
    ser.write(buf)



def send_settings(ser, brightness):

    set = "B%3d"%brightness
    ser.write(bytearray([1, 1]))
    ser.write(set)
    padding = [0] * (16*3-len(set))
    ser.write(padding)

    print "Sent: "+set
    # print "Responce: ", ser.readline()

def send_time(ser):

    dt = str(long(time.time()) - time.timezone)
    ser.write(bytearray([2, 1]))
    ser.write(dt)
    padding = [0] * (16*3-len(dt))
    ser.write(padding)
    ser.flush()
    print "Time Sent: "+dt
    # print "Responce: ", ser.readline()

def run(ser):
    imgs = []
    imgs.append(cv2.imread("/home/padeler/Desktop/frog.png"))
    imgs.append(cv2.imread("/home/padeler/Desktop/mario.jpg"))

    test = np.zeros((16,16,3), dtype=np.ubyte)
    test[:, :] = [0,20,0]

    imgs.append(test)
    frames = itertools.cycle(imgs)
    k=0
    sleep_time = 100
    for f in frames:

        bf = cv2.resize(f, (160, 160), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("IMG", bf)

        send_image(ser, f)
        # time.sleep(1)
        # read(ser)

        t = time.time()
        k = cv2.waitKey(sleep_time)
        if k & 0xFF == ord('q'):
            break

        dt = time.time() - t
        print "DT: ", dt
        # time.sleep(max(0, 1.0-dt))

    time.sleep(2)
    img = np.zeros((16, 16, 3), dtype=np.ubyte)
    send_image(ser, img)
    time.sleep(1)
    read(ser)


def test(ser):

    ser.write(bytearray([10,2,0,0,0,0,0,0]))
    time.sleep(2)
    read(ser)
    time.sleep(2)


if __name__ == '__main__':
    ser = serial.Serial("/dev/ttyUSB0", 115200, dsrdtr=True)
    # ser = serial.Serial("/dev/ttyUSB0", 500000)
    time.sleep(2)
    # print ser
    send_time(ser)
    # test(ser)
    time.sleep(1)
    # read(ser)
    # send_settings(ser, 20)
    # run(ser)

    time.sleep(1)
    read(ser)
    # ser.close()