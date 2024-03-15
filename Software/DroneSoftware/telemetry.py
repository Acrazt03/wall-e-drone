
def run():
    telemetry_port = '/dev/ttyTHS0'
    default_telemetry_address = 'udp:192.168.177.156:10000'
    telemetry_proccess = subprocess.Popen(["mavproxy.py", "--master", telemetry_port, "--out", default_telemetry_address, "--baudrate", baud_rate, "--nowait", "--daemon"])

if __name__ == '__main__':
    run()