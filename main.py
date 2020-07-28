from test import floorNet

if __name__ == "__main__":

    if sys.argv[1] == '--test':
        if sys.argv[2] == 'debug':
            floorNet.infer(debug=True)
        if sys.argv[2] == 'infer':
            floorNet.infer(debug=False)

    else:
        print("Error: Invalid option!")
