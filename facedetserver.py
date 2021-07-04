import socket
import time
import msgpack
import magic
import threading



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
                chunk = self.socket.recv(4096)
                if chunk == b'':
                    print('Client disconnected from', address)
                    break
                unpacker.feed(chunk)
                for unpacked in unpacker:
                    img, meta = unpacked
                    # cutoff the faces under confidence
                    faces = filter(lambda x: x[b'cnf'] > self.confidence_cutoff)
                    # print('Matches -> ', meta)
                    # print(magic.from_buffer(img))
                    self.datastore.set({'img': img, 'faces': faces})