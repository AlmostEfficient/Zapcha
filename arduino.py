import serial
import time
ser = serial.Serial('/dev/ttyACM1', baudrate = 9600, timeout = 1)

def setValues():
    while True:
        print('writing')
        ser.write(b'100')
        time.sleep(1)
        ser.write(b'0\n')
        time.sleep(1)

    arduinoData = ser.readline().decode('ascii')
    return arduinoData

while (1):
    userInput = input('Set data point?')
    if userInput == 'y':
        print(setValues())

# while 1:
#     arduinoData = ser.readline().decode('ascii')
#     print(arduinoData)