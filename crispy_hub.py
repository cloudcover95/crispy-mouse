import serial
import serial.tools.list_ports
import time
import sys

def find_mcu():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if any(x in port.device for x in ["usbmodem", "USB", "ACM"]):
            return port.device
    return None

def main():
    print("=== Crispy Mouse Hub (JuniorCloud LLC) ===")
    port_name = find_mcu()
    if not port_name:
        print("Error: No ATmega32U4 found.")
        sys.exit(1)

    ser = serial.Serial(port_name, 115200, timeout=1)
    time.sleep(2)

    while True:
        print("\n[1] Set Sensitivity  [2] Set Damping  [3] Set Threshold  [0] Exit")
        choice = input("Select: ")
        if choice == '1':
            val = input("Value (e.g. 2.5): ")
            ser.write(f"SENS:{val}\n".encode())
        elif choice == '2':
            val = input("Value (0.01-1.0): ")
            ser.write(f"DAMP:{val}\n".encode())
        elif choice == '3':
            val = input("Value (0-1023): ")
            ser.write(f"THRE:{val}\n".encode())
        elif choice == '0':
            break
    ser.close()

if __name__ == "__main__":
    main()
