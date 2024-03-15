import logging
from subsystems.utils import displayPrintLine, check_internet_conn, check_fc
import time
import subprocess
import sys

wait_sec = 15
print(f'Waiting for {wait_sec} secs...')
time.sleep(wait_sec)

logging.basicConfig(level=logging.DEBUG, filemode="a+", filename='logfile',
                        format="%(asctime)-15s %(levelname)-8s %(message)s")

logging.info("wall-e ran!")

try:
    displayPrintLine('Wall-E', duration=5)
    logging.info("wall-e sent the request")
except Exception as e:
    logging.info('wall-e had this Exception: ' + str(e))

#Check if there is internet connection
print('Checking Internet Connection')
displayPrintLine('Check INTERNET_CONN')

if check_internet_conn():
    displayPrintLine('INTERNET_CONN OK')
    logging.info('Device has internet connectivity OK')
else:
    displayPrintLine('ERROR NO INTERNET')
    logging.error('DEVICE NOT CONNECTED TO THE INTERNET')

    displayPrintLine('WAIT CONNECTION')
    logging.info('Waiting for internet connection!')

    while not check_internet_conn():
        displayPrintLine('Connecting...')
        time.sleep(1)
    
    displayPrintLine('INTERNET_CONN OK')
    logging.info('Device has internet connectivity OK')

baud_rate = "57600"

#Check if the FC is connected
print('Checking FC')

fc_port = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400f3WS-if00-port0'

displayPrintLine('Check FC')
logging.info('Connecting to FC')

if check_fc(fc_port):
    logging.info('FC OK')
else:
    logging.error('FC NOT CONNECTED')
    displayPrintLine('Waiting for FC conn')

    while not check_fc(fc_port):
        displayPrintLine('Connecting to FC...')
        time.sleep(1)
    
    logging.info('FC OK')

#   Start sending telemetry (mavproxy) to the default ip
displayPrintLine('Check Telemetry')
logging.info('Connecting to telemetry FC')

print('Checking Telemetry')

telemetry_port = '/dev/ttyTHS0'
destination_address = 'udp:181.36.43.138:10000'

if check_fc(port=telemetry_port):
    logging.info('Telemetry OK')
else:
    logging.error('Telemetry NOT CONNECTED')
    displayPrintLine('Waiting for Telemetry conn')

    while not check_fc(port=telemetry_port):
        displayPrintLine('Connecting to Telemetry...')
        time.sleep(1)
    
    logging.info('Telemetry OK')

displayPrintLine('START TELEMETRY')
telemetry_proccess = subprocess.Popen(["mavproxy.py", "--master", telemetry_port, "--out", destination_address, "--baudrate", baud_rate, "--nowait", "--daemon"])

while True:
    print('here')
    time.sleep(1)

#Connect to MQTT
#Start listenning for MQTT cmds

logging.info("wall-e finished")

#Subsytems
"""
1. Flight Controller (PixHawk)
    1.1. Camera Gimabal
    1.2. Gripper
    1.3. Flight itself
2. 4G Module
3. Wifi Module
4. OLED Display
5. Camera
"""
