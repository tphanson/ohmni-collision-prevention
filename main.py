import sys
import socket
from test import floorNet

# Init botshell
botshell = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
botshell.connect("/app/bot_shell.sock")
botshell.sendall(b"wake_head\n")

if __name__ == "__main__":

    if sys.argv[1] == '--test':
        if sys.argv[2] == 'debug':
            floorNet.infer(botshell, debug=True)
        if sys.argv[2] == 'infer':
            floorNet.infer(botshell, debug=False)

    else:
        print("Error: Invalid option!")
