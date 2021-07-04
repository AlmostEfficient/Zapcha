import socket
import time
import msgpack
import magic
import threading

import base64
import cv2
import json
import numpy as np




class FaceDetectServer(threading.Thread):
    def __init__(self, datastore, confidence_cutoff=70):
        self.datastore = datastore
        self.confidence_cutoff = confidence_cutoff
        super().__init__()
        self.daemon = True

    def run(self, *args, **kwargs):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(("", 7071))
        serversocket.listen(5)
        while True:
            # accept connections from outside
            (clientsocket, address) = serversocket.accept()
            print('Client connected from', address)
            # now do something with the clientsocket
            # in this case, we'll pretend this is a threaded server
            unpacker = msgpack.Unpacker(raw=True)
            while True:
                chunk = clientsocket.recv(4096)
                if chunk == b'':
                    print('Client disconnected from', address)
                    break
                unpacker.feed(chunk)
                for unpacked in unpacker:
                    imgdata, meta = unpacked
                    # convert img into legacy cut image

                    split_w = 3
                    split_h = 3

                    nparr = np.fromstring(imgdata, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    return_list = []
                    for i in range(split_h):
                        for j in range(split_w):
                            cropped = frame[i*(frame.shape[0]//split_h):(i+1)*(frame.shape[0]//split_h),j*(frame.shape[1]//split_w):(j+1)*(frame.shape[1]//split_w)]
                            frame_str = cv2.imencode('.jpg', cropped)[1]
                            frame_str = base64.b64encode(frame_str)
                            return_list.append(str(frame_str)[2:].strip("'"))

                    # cutoff the faces under confidence
                    faces = filter(lambda x: x[b'cnf'] > self.confidence_cutoff, meta)
                    # print('Matches -> ', meta)
                    # print(magic.from_buffer(img))
                    with self.datastore.mutex:
                        self.datastore.data.update({'img': {'data':return_list}, 'faces': faces})