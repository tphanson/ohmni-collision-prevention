import time
import random
from threading import Thread

POSSIBLE_MOVES = [(500, -500), (-500, 500), (500, 500), (-500, -500),
                  (500, 0), (0, 500), (-500, 0), (0, -500)]


def _move_cmd(signal):
    (lw, rw) = signal
    return f'manual_move {lw} {rw}\n'.encode()


def _simMovement(botshell):
    while True:
        counter = 0
        random_signal = random.choice(POSSIBLE_MOVES)
        cmd = _move_cmd(random_signal)
        while counter < 100:
            counter += 1
            botshell.sendall(cmd)
            time.sleep(0.01)


def simMovement(botshell):
    t = Thread(target=_simMovement, args=(botshell, ), daemon=True)
    t.start()
