import os.path
import serial

def get_ports():
    ports = [serial.device(i) for i in range(5)]
    if os.name == "posix":
        for device in ["/dev/ttyUSB%d" % i for i in range(5)]:
            if os.path.exists(device):
                ports.append(device)
    return ports

def get_speeds():
    return [9600, 19200, 38400, 57600, 115200]
