from pymavlink import mavutil
from utils import displayPrintLine, MQTTConnection, periodicTask
from threading import Thread, Lock
import sys
import json
import time 
from collections import deque
import copy

class FlightController():
    SERIAL_PORT = '/dev/ttyTHS0'
    source_system = 255
    baudrate = 57600
    force_connected = False
    isPublishingTelemetry = True
    #last_msg = None

    def __init__(self):
        displayPrintLine('Connecting to FC...')

        try:
            self.master = mavutil.mavlink_connection(self.SERIAL_PORT, autoreconnect=True,
                                        source_system=self.source_system,
                                        baud=self.baudrate,
                                        force_connected=self.force_connected)

            if self.master.wait_heartbeat(timeout=1) == None:
                raise Exception("ERROR: FC has no Heartbeat!") 
                exit()

        except Exception as e:
            print(e)
            displayPrintLine(str(e))
            exit()
        
        displayPrintLine('Connected to FC!')

        #To don't allow multiple threads to access the serial port at the same time
        #self.master.lock = Lock()

        self.startSendingHeartbeat()

        self.mqttConnection = MQTTConnection()
        print(self.mqttConnection.client)
        self.mqttConnection.connect()

        if self.mqttConnection.isConnected():
            self.startPublishingTelemetry()

        self.serial_buffer = deque(maxlen=100)

    def sendHeartbeat(self):
            self.master.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,
                                                    mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)

    def startSendingHeartbeat(self):
        #Send heartbeat to FC at 1hz
        thread = Thread(target=periodicTask, args=(self.sendHeartbeat,1))
        thread.start()

    def startPublishingTelemetry(self):
        self.isPublishingTelemetry = True
        rate = 1
        startSending = 1 #1 Start, 0 Stop
        self.master.mav.request_data_stream_send(self.master.target_system,
                                                self.master.target_component,
                                                mavutil.mavlink.MAV_DATA_STREAM_ALL,rate,startSending)

        thread = Thread(target=self.receiveMAVlinkMSGs)
        thread.start()

    def stopPublishingTelemetry(self):
        self.isPublishingTelemetry = False
        rate = 1
        startSending = 0 #1 Start, 0 Stop
        self.master.mav.request_data_stream_send(self.master.target_system,
                                                self.master.target_component,
                                                mavutil.mavlink.MAV_DATA_STREAM_ALL,rate,startSending)

    def receiveMAVlinkMSGs(self):
        while True:
            msg = self.master.recv_match(blocking=True)
            #self.last_msg = msg
            if not msg:
                return
            if msg.get_type() == "BAD_DATA":
                print(msg.get_type())
                #if mavutil.all_printable(msg.data):
                #    sys.stdout.write(msg.data)
                #    sys.stdout.flush()
            else:

                self.serial_buffer.append(msg)

                if self.isPublishingTelemetry:
                    
                    #TODO: BE MORE SELECTIVE ABOUT WHAT INFO IS NEEDED to reduce traffic
                    data = json.dumps(msg.to_dict())
                    
                    #TODO: Disabled for now
                    #success = self.mqttConnection.publish('TELEMETRY', data)

                    #if not success:
                    #    printLine("ERROR MQTT Broker")
 
    def recv_match(self, msg_type, condition=lambda x: True, timeout=None):
        
        start_time = time.time()

        while True:

            if timeout is not None:
                now = time.time()
                if now < start_time:
                    start_time = now # If an external process rolls back system time, we should not spin forever.
                if start_time + timeout < time.time():
                    return None

            #To prevent: RuntimeError: deque mutated during iteration
            #serial_buffer = copy.deepcopy(self.serial_buffer)

            for msg in list(self.serial_buffer):
                if msg.get_type() == msg_type and condition(msg):
                    #self.serial_buffer.remove(msg)
                    return msg
    
    def send_long_cmd(self, cmd):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            cmd.cmd_id,
            cmd.confirmation,
            cmd.param1,cmd.param2,cmd.param3,cmd.param4,cmd.param5,cmd.param6,cmd.param7)  

        def check_if_is_my_cmd(msg):
            return msg.command == cmd.cmd_id

        cmd_ack = self.recv_match('COMMAND_ACK', condition=check_if_is_my_cmd, timeout=20)
        return cmd_ack

import uvicorn
from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()
app.fc = FlightController()

@app.get('/telemetry/')
async def getTelemetry(msg_type: str = 'HEARTBEAT'):
    msg = app.fc.recv_match(msg_type, timeout=5)
    if msg != None:
        return msg.to_dict()
    else:
        return None

#master.mav.command_long_send(
#        master.target_system,
#        master.target_component,
#        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
#        0,
#        1, 0, 0, 0, 0, 0, 0)

#mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM

class LongCommand(BaseModel):
    cmd_id: int
    confirmation: Optional[int] = 0
    param1: Optional[float] = 0
    param2: Optional[float] = 0
    param3: Optional[float] = 0
    param4: Optional[float] = 0
    param5: Optional[float] = 0
    param6: Optional[float] = 0
    param7: Optional[float] = 0

@app.post('/longCMD/')
async def sendCMD(longCMD: LongCommand):
    cmd_ack = app.fc.send_long_cmd(longCMD)
    if cmd_ack != None:
        return cmd_ack.to_dict()
    else:
        return None

if __name__ == "__main__":
    uvicorn.run(app, port=5002)