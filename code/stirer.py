import serial.tools.list_ports

# List all available serial ports
ports = serial.tools.list_ports.comports()

# Check if any serial ports are available
if not ports:
    print("No serial ports found.")
else:
    print("Available serial ports:")
    for port in ports:
        print(f"Port: {port.device}, Description: {port.description}")
