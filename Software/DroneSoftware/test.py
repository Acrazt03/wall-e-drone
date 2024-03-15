from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException
import time

port = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400f3WS-if00-port0'
baudrate = 57600

vehicle = connect(port, baud=baudrate,wait_ready=True)

while vehicle.is_armable!=True:
    print("Waiting for vehicle to become armable.")
    time.sleep(1)
print("Vehicle is now armable")