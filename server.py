import cv2
import base64
from flask import jsonify
from flask_cors import CORS
from flask import Flask
app = Flask(__name__)

cap = cv2.VideoCapture(0)
if(not cap):
    print("camera unable to open")
split_h = 3
split_w = 3
"""
while True:
    ret, frame = cap.read()
    return_list = []
    if(ret):
        for i in range(split_w):
            for j in range(split_h):
                #cv2.imshow('frame{} {}'.format(i,j),frame[i(frame.shape[0]//split_h):(i+1)(frame.shape[0]//split_h),j(frame.shape[1]//split_w):(j+1)(frame.shape[1]//split_w)])
                return_list.append(frame[i(frame.shape[0]//split_h):(i+1)(frame.shape[0]//split_h),j(frame.shape[1]//split_w):(j+1)(frame.shape[1]//split_w)])
    else:
        break
    key = cv2.waitKey(1)
    if(key==ord('q')):
        break
cv2.destroyAllWindows()
cap.release()
"""
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
        return "error"
    return jsonify(return_list)

if __name__=="__main__":
    CORS(app)
    app.run("0.0.0.0")
    print("Running server")
    cap.release()
