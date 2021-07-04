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
        img = datastore.data.get('img')
    if img is None:
        return 404
    return send_file(io.BytesIO(img), mimetype='image/jpeg')

def check_intersect_squares(guess, face):
    # find the overlap
    dx = min(guess['x'] + guess['w'], face['x'] + face['w']) - max(guess['x'], face['x'])
    dy = min(guess['y'] + guess['h'], face['y'] + face['h']) - max(guess['y'], face['y'])
    if dx < 0 or dy < 0:
        return False  # no match
    if face['w'] > guess['w']:
        # handle when face is larger than guess size
        comp_w = guess['w']
    else:
        comp_w = face['w']

    if face['h'] > guess['h']:
        # handle when face is larger than guess size
        comp_h = guess['h']
    else:
        comp_h = face['h']

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
            faces = datastore.get('faces', [])
        guess = request.get_json()
        # run calculations here
        correct = check_user_guess(guess, faces)
        if correct:
            datastore.shoot_queue.push(guess)
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


