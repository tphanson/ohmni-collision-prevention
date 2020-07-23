import sys
import os
import socket
from test import floorNet


if os.path.exists("/dev/libcamera_stream"):
    os.remove("/dev/libcamera_stream")

# Init botshell
botshell = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
botshell.connect("/app/bot_shell.sock")
botshell.sendall(b"wake_head\n")
# Init camera server
print("Opening socket...")
server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
server.bind("/dev/libcamera_stream")
os.chown("/dev/libcamera_stream", 1047, 1047)


if __name__ == "__main__":

    if sys.argv[1] == '--test':
        if sys.argv[2] == 'infer':
            floorNet.infer(server)

    else:
        print("Error: Invalid option!")
