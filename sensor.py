import sys
import glob
import time
import serial
import warnings

BAUDRATE = 115200
VERSION = 'sensor_v1\r\n'.encode()
NUM_BITS = 12

# Commands
VER = 'V'.encode()
ANGLE = 'A'.encode()


class CrankAngleSensor(object):
    def __init__(self):
        self._sensor = self._get_sensor()

    @staticmethod
    def _get_sensor():
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        results = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.baudrate = BAUDRATE
                s.timeout = 1
                time.sleep(2)  # Wait until everything is set up
                s.write(VER)
                s.flush()
                version = s.readline()
                if version == VERSION:
                    results.append(s)
                else:
                    s.close()
            except (OSError, serial.SerialException):
                pass
        if not len(results):
            raise RuntimeError('No supported sensor was found. Make sure that '
                               'it is plugged in and the COM port is closed')
        elif len(results) is not 1:
            warnings.warn('More than one supported sensors are connected. '
                          'Using the one on COM{}'.format(results[0].port))
        return results[0]

    def get_angle(self):
        self._sensor.write(ANGLE)
        self._sensor.flush()
        angle_string = self._sensor.readline().decode().rstrip()
        angle_float = 360 / 2 ** NUM_BITS * float(angle_string)
        return angle_float
