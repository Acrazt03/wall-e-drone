from utils import displayPrintLine
from pymavlink import mavutil

source_system = 255
baudrate = 57600
force_connected = False
port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400f3WS-if00-port0'

the_connection = mavutil.mavlink_connection(port, autoreconnect=True,
                                        source_system=source_system,
                                        baud=baudrate,
                                        force_connected=force_connected)

if the_connection.wait_heartbeat(timeout=2) == None:
    displayPrintLine("ERROR: FC has no Heartbeat!")
    print('ERROR: FC has no Heartbeat!')
    the_connection.close()
    exit(1)
else:
    displayPrintLine('Connected to FC!')
    print('Connected to FC!')

the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)