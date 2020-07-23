import sys
from test import floorNet


if __name__ == "__main__":

    if sys.argv[1] == '--test':
        if sys.argv[2] == 'debug':
            floorNet.infer(True)
        if sys.argv[2] == 'infer':
            floorNet.infer(False)

    else:
        print("Error: Invalid option!")
