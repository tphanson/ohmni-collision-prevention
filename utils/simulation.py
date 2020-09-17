import time
import random
from threading import Thread
import numpy as np


def _simMovement(botshell):
    counter = 0
    while counter < 10:
        counter += 1
        botshell.sendall(b'manual_move 500 -500\n')
        time.sleep(1)


def simMovement(botshell):
    t = Thread(target=_simMovement, args=(botshell, ))
    t.start()
