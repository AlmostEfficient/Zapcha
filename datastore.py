import threading
import queue
import threading

class ItemStore(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.items = []

    def add(self, item):
        with self.lock:
            self.items.append(item)

    def get_all(self):
        with self.lock:
            items, self.items = self.items, []
        return items

class Datastore:
    IMAGE_WIDTH = 480
    IMAGE_HEIGHT = 480
    SERVO_X_DIR = 1
    SERVO_Y_DIR = 1
    SERVO_X_MIN = 60
    SERVO_X_MAX = 120
    SERVO_Y_MIN = 60
    SERVO_Y_MAX = 120



    def __init__(self, *args, **kwargs):
        self.mutex = threading.Lock()
        self.data = dict()
        self.shoot_queue = ItemStore()