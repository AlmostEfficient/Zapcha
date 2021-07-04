import threading
import queue

class Datastore:
    IMAGE_WIDTH = 640
    IMAGE_HEIGHT = 480
    SERVO_X_DIR = 1
    SERVO_Y_DIR = 1
    SERVO_X_MIN = 0
    SERVO_X_MAX = 180
    SERVO_Y_MIN = 0
    SERVO_Y_MAX = 180



    def __init__(self, *args, **kwargs):
        self.mutex = threading.Lock()
        self.data = dict()
        self.shoot_queue = queue.Queue()