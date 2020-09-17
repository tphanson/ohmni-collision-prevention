import time
import random
from threading import Thread
import numpy as np


def _simMovement(botshell):
    while True:
        botshell.sendall(b'manual_move 500 -500\n')
        time.sleep(0.01)


def simMovement(botshell):
    t = Thread(target=_simMovement, args=(botshell, ))
    t.start()
