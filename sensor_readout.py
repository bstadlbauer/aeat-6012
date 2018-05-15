from serial.tools import list_ports
import serial


class Sensor(object):
    def __init__(self):
        port = self._find_sensor_port()

    def _find_sensor_port(self):
        port_list = list_ports
        print(port_list)
        port = port_list[0]
        return

    def get_crank_angle(self):
        pass