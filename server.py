import cv2
import base64
import json
from flask import jsonify
from flask_cors import CORS
from flask import Flask
from flask import request, send_file
import serial
import time
import io

from facedetserver import FaceDetectServer
from datastore import Datastore
from cannon import CannonController

app = Flask(__name__)
datastore = Datastore()
facedet = FaceDetectServer(datastore)
cannon = CannonController(datastore)

@app.route('/')
def main():
    return "hi"
@app.route('/frame')
def frame():
    with datastore.mutex:
        img_split = datastore.data.get('img')
    if img_split is None:
        return 404
    return img_split

# def frame():
#     global cap
#     ret, frame = cap.read()
#     return_list = []
#     if(ret):
#         for i in range(split_w):
#             for j in range(split_h):
#                 cropped = frame[i*(frame.shape[0]//split_h):(i+1)*(frame.shape[0]//split_h),j*(frame.shape[1]//split_w):(j+1)*(frame.shape[1]//split_w)]
#                 frame_str = cv2.imencode('.jpg', cropped)[1]
#                 frame_str = base64.b64encode(frame_str)
#                 return_list.append(str(frame_str)[2:].strip("'"))
#     if(not ret):
#         print("error")
#         return "error"
#     return jsonify(return_list)
#     if img is None:
#         return 404
#     return send_file(io.BytesIO(img), mimetype='image/jpeg')

def check_intersect_squares(guess, face):
    # find the overlap
    print(guess, face)
    dx = min(guess['x'] + guess['w'], face[b'x'] + face[b'w']) - max(guess['x'], face[b'x'])
    dy = min(guess['y'] + guess['h'], face[b'y'] + face[b'h']) - max(guess['y'], face[b'y'])
    if dx < 0 or dy < 0:
        return False  # no match
    if face[b'w'] > guess['w']:
        # handle when face is larger than guess size
        comp_w = guess['w']
    else:
        comp_w = face[b'w']

    if face[b'h'] > guess['h']:
        # handle when face is larger than guess size
        comp_h = guess['h']
    else:
        comp_h = face[b'h']

    return (dx > comp_w / 2) and (dy > comp_h / 2)


def check_user_guess(guess, faces):
    """Check user guess

    args:
    - guess: dict {x: int, y: int}
    - faces: array of dicts
        {b'cnf': int, b'h': int, b'w': int, b'x': int, b'y': int}
    """
    guess_pixels = {
        'x': guess['x'] * datastore.IMAGE_WIDTH / 3,
        'y': guess['y'] * datastore.IMAGE_HEIGHT / 3,
        'w': datastore.IMAGE_WIDTH / 3,
        'h': datastore.IMAGE_HEIGHT / 3,
    }

    for face in faces:
        if check_intersect_squares(guess_pixels, face):
            return True
    return False



@app.route('/shoot', methods=['POST'])
def shoot():
    if request.method =='POST':
        with datastore.mutex:
            faces = datastore.data.get('faces', [])
        guess = request.get_json()
        guess = json.loads(guess)
        guess = list(filter(lambda x: x[1] == True, guess.items()))[0][0]
        
        CONVERSION = {
            0: {'x': 0, 'y': 2},
            1: {'x': 1, 'y': 2},
            2: {'x': 2, 'y': 2},
            3: {'x': 0, 'y': 1},
            4: {'x': 1, 'y': 1},
            5: {'x': 2, 'y': 1},
            6: {'x': 0, 'y': 0},
            7: {'x': 1, 'y': 0},
            8: {'x': 2, 'y': 0},
        }

        guess = CONVERSION[int(guess)]

        # run calculations here
        correct = check_user_guess(guess, faces)
        correct=True
        if correct:
            datastore.shoot_queue.add(guess)
            return {'success': False}
        else:
            return {'success': True}
    else:
        return 403

if __name__=="__main__":
    CORS(app)
    facedet.start()
    cannon.start()
    app.run("0.0.0.0")
    print("Running server")
    # cap.release()


