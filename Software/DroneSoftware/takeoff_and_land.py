from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException
import time
#import socket
#import exceptions
#import math

##Function to arm the drone props and takeoff at targetHeight (m)
def arm_and_takeoff(targetHeight):

	while vehicle.is_armable!=True:
		print("Waiting for vehicle to become armable.")
		time.sleep(1)
	print("Vehicle is now armable")

	vehicle.mode = VehicleMode("GUIDED")

	while vehicle.mode!='GUIDED':
		print("Waiting for drone to enter GUIDED flight mode")
		time.sleep(1)
	print("Vehicle now in GUIDED MODE. Have fun!!")

	vehicle.armed = True
	while vehicle.armed==False:
		print("Waiting for vehicle to become armed.")
		time.sleep(1)
	print("Look out! Virtual props are spinning!!")

	vehicle.simple_takeoff(targetHeight)

	while True:
		print("Current Altitude: %d"%vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.alt>=.95*targetHeight:
			break
		time.sleep(1)
	print("Target altitude reached!!")

	return None

port = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400f3WS-if00-port0'
baudrate = 57600

vehicle = connect(port, baud=baudrate,wait_ready=True)

arm_and_takeoff(2)
print("Vehicle reached target altitude")

vehicle.mode=VehicleMode('LAND')
while vehicle.mode!='LAND':
	print("Waiting for drone to enter LAND mode")
	time.sleep(1)
print("Vehicle now in LAND mode. Will touch ground shortly.")