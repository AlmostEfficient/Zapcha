import cv2
import base64
import json
from flask import jsonify
from flask_cors import CORS
from flask import Flask
from flask import request
import serial
import time 

app = Flask(__name__)

cap = cv2.VideoCapture(0)

if(not cap):
    print("camera unable to open")
split_h = 3
split_w = 3

@app.route('/')
def main():
    return "hi"
@app.route('/frame')
def frame():
    global cap
    ret, frame = cap.read()
    return_list = []
    if(ret):
        for i in range(split_w):
            for j in range(split_h):
                cropped = frame[i*(frame.shape[0]//split_h):(i+1)*(frame.shape[0]//split_h),j*(frame.shape[1]//split_w):(j+1)*(frame.shape[1]//split_w)]
                frame_str = cv2.imencode('.jpg', cropped)[1]
                frame_str = base64.b64encode(frame_str)
                return_list.append(str(frame_str)[2:].strip("'"))
    if(not ret):
        print("error")
        return "error"
    return jsonify(return_list)


ser = serial.Serial('/dev/ttyACM1', baudrate = 9600, timeout = 1)

def setValues():
    while True:
        print('writing')
        ser.write(b'100')
        time.sleep(1)
        ser.write(b'0\n')
        time.sleep(1)

@app.route('/shoot', methods=['POST'])
def shoot():
    if request.method =='POST':
        payload = request.get_json()
        data = json.loads(payload) #This is a dict
        targets = [] # This is a list of numbers that correspond to the grid (0-8)
        for item in data:
            if data[item] is True:
                targets.append(item)
        targetString= (', ').join(targets)
        
        
        return jsonify({"response":'Shooting points '+ targetString}), 200
    else:
        return 403

if __name__=="__main__":
    CORS(app)
    app.run("0.0.0.0")
    print("Running server")
    cap.release()

coordinates = {0: "1,1", 1:"0,1", "2":"1,1", 3:"1,1", 4:"1,0", }

coordinates.get(0)


