import threading
import serial
from serial.tools import list_ports
import time
import random
import numpy as np
from config import config

makcu = None
makcu_lock = threading.Lock()
button_states = {i: False for i in range(5)}
is_connected = False
last_value = 0
baud_change_command = bytearray([0xDE, 0xAD, 0x05, 0x00, 0xA5, 0x00, 0x09, 0x3D, 0x00])

SUPPORTED_DEVICES = [
    ("1A86:55D3", "MAKCU"),
    ("1A86:7523", "CH340"),
    ("1A86:5523", "CH343"),
    ("1A86:5740", "CH347"),
    ("10C4:EA60", "CP2102"),
]
BAUD_RATES = [4000000, 2000000, 115200]

def find_com_ports():
    found_ports = []
    for port in list_ports.comports():
        hwid = port.hwid.upper()
        desc = port.description.upper()
        for vidpid, name in SUPPORTED_DEVICES:
            if vidpid in hwid or name in desc:
                found_ports.append((port.device, name))
    return found_ports

def connect_to_makcu():
    global makcu, is_connected
    found_ports = find_com_ports()
    if not found_ports:
        print("[ERROR] No supported serial devices found.")
        return False

    for port, dev_name in found_ports:
        for baud in BAUD_RATES:
            try:
                print(f"[INFO] Trying {dev_name} on {port} at {baud} baud...")
                makcu = serial.Serial(port, baud, timeout=0.1)
                time.sleep(1)
                if dev_name == "MAKCU" and baud == 115200:
                    makcu.write(baud_change_command)
                    makcu.close()
                    print("[INFO] Makcu initialized with 4 Million baud rate.")
                    makcu = serial.Serial(port, 4000000, timeout=0.1)
                    makcu.baudrate = 4000000
                with makcu_lock:
                    makcu.write(b"km.buttons(1)\r")
                    makcu.flush()
                is_connected = True
                print(f"[INFO] Connected to {dev_name} on {port} at {makcu.baudrate} baud.")
                return True
            except serial.SerialException as e:
                print(f"[WARN] Failed to connect to {dev_name} on {port} at {baud} baud: {e}")
                if makcu:
                    makcu.close()
                makcu = None
    print("[ERROR] Could not connect to any supported device.")
    return False

def count_bits(n: int) -> int:
    return bin(n).count("1")

def listen_makcu():
    global last_value, button_states
    while is_connected:
        try:
            if makcu.in_waiting > 0:
                byte = makcu.read(1)
                if not byte:
                    continue
                value = byte[0]

                if value > 31 or (value != 0 and count_bits(value) != 1):
                    continue

                newly_pressed = (value ^ last_value) & value
                newly_released = (value ^ last_value) & last_value

                for i in range(5):
                    if newly_pressed == (1 << i):
                        button_states[i] = True
                    elif newly_released == (1 << i):
                        button_states[i] = False

                last_value = value

        except serial.SerialException as e:
            print(f"[ERROR] SerialException in listener thread: {e}")
            break

def send_click_command():
    if not is_connected:
        return

    if getattr(config, "random_delay_enabled", False):
        delay = random.uniform(0.01, 0.05)
        time.sleep(delay)

    with makcu_lock:
        makcu.write(b"km.left(1)\r km.left(0)\r")
        makcu.flush()

    time.sleep(config.shooting_rate / 1000)

class Mouse:
    def __init__(self):
        global is_connected
        if not is_connected:
            if not connect_to_makcu():
                print("[ERROR] Could not connect to any supported device.")
                return
            else:
                listener_thread = threading.Thread(target=listen_makcu, daemon=True)
                listener_thread.start()

    def click(self):
        send_click_command()
