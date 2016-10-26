__author__ = 'Taavi'

import threading
import logging
import time

class TestThread(threading.Thread):

    def __init__(self, func, txt):
        threading.Thread.__init__(self)
        self.func = func
        self.txt = txt

    def run(self):
        while True:
            self.func(self.txt)
            time.sleep(1)