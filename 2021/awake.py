from threading import Timer as sched
from pynput.keyboard import Key as key_key, Controller as key_control
class awake:
    def __init__(self, refresh_rate=120):
        self.active = True
        self.top = (__name__ == '__main__')
        self.counter = ''
        self.timeout = refresh_rate
        self.keyboard = key_control()
        self.loop()
    def loop(self):
        self.keyboard.press(key_key.num_lock)
        self.keyboard.release(key_key.num_lock)
        self.keyboard.press(key_key.num_lock)
        self.keyboard.release(key_key.num_lock)
        if self.active:
            if self.top:
                print('\r{}'.format(self.counter),end='')
                self.counter += '█'
            self.thread = sched(self.timeout, self.loop)
            self.thread.start()
    def stop(self):
        self.active = False
        self.thread.cancel()
if __name__ == '__main__':
    awake()
