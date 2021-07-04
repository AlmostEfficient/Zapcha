import serial
import threading
import struct

from collections import defaultdict

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


class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

def most_frequent(items):
    if len(items) == 0:
        return None
    count = defaultdict(int)
    for item in items:
        item = hashabledict(item)
        count[item] += 1
    return sorted(count.items(), key=lambda x: x[1], reverse=True)[0][0]

def guess_to_servo_coords(guess, config):
    return {
        'x': (config.SERVO_X_MAX - config.SERVO_X_MIN) / 3 * guess['x'],
        'y': (config.SERVO_Y_MAX - config.SERVO_Y_MIN) / 3 * guess['y']
    }



class CannonController(threading.Thread):
    def __init__(self, datastore, tty='/dev/ttyACM1', baudrate=9600, timeout=1):
        self.datastore = datastore
        self.shoot_queue = ItemStore()
        self.tty = tty
        self.baudrate = baudrate
        self.timeout = timeout
        super().__init__()
        self.daemon = True


    def run(self, *args, **kwargs):
        self.serial = serial.Serial(self.tty, baudrate=self.baudrate, timeout=self.timeout)

        while True:
            self.datastore.tick.wait()

            shoot_options = self.shoot_queue.get_all()
            if len(shoot_options) == 0:
                continue
            chosen = most_frequent(shoot_options)
            servo_coords = guess_to_servo_coords(chosen)

            self.serial.write('{:03d},{:03d}\n'.format(servo_coords['x'], servo_coords['y']))
            # self.serial.write('FIRE')
            # self.serial.write(struct.pack(servo_coords['x']))
            # self.serial.write(struct.pack(servo_coords['y']))

            print(self.serial.read_all())