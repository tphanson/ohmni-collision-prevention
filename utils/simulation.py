import time
import random
from threading import Thread
import numpy as np

POSSIBLE_MOVES = [(500, -500), (0, 0), (-500, 500),
                  (500, 0), (0, 500), (-500, 0), (0, -500),
                  (500, 500), (-500, -500)]


def _move_cmd(signal):
    (lw, rw) = signal
    return f'manual_move {lw} {rw}\n'


def _simMovement(botshell):
    while True:
        random_signal = random.choice(POSSIBLE_MOVES)
        cmd = _move_cmd(random_signal)
        botshell.sendall(cmd)
        time.sleep(0.01)


def simMovement(botshell):
    t = Thread(target=_simMovement, args=(botshell, ))
    t.start()
