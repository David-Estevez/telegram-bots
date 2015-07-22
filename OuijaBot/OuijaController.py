pronterface_path = '/home/def/Repositories/Printrun'

import sys, time
sys.path.append(pronterface_path)

from printrun.printcore import printcore
from printrun import gcoder

from Calibration import ouijamap

class OuijaController:
    def __init__(self, port, baudrate, magnet1_pin=4, magnet2_pin=5, config_file=None):
        self.port = port
        self.baudrate = baudrate
        self.magnet1_pin = magnet1_pin
        self.magnet2_pin = magnet2_pin
        self.config_file = config_file

        self.magic_table = printcore()

    def connect(self):
        time.sleep(2)
        print '[OuijaController] Connecting to device... '
        self.magic_table.connect(self.port, self.baudrate)
        time.sleep(2)
        if self.magic_table.online:
            print '[OuijaController] Connected!'
        else:
            raise Exception('Could not connect to device! (Port: %s, Baudrate: %s)' % (self.port, self.baudrate))

        # Homing
        print '[OuijaController] Homing...'
        self.magic_table.send("G28 Y0\nG28 X0\n")

        return True

    def disconnect(self):
        self.magic_table.disconnect()
        if not self.magic_table.online:
            print '[OuijaController] Disonnected!'
            return True
        else:
            raise Exception('Could not disconnect the device!')

    def go_to(self, token):
        try:
            x,y = ouijamap[token]
        except:
            print '[OuijaController] Token: %s is not printable on OuijaTable' % token
            return False

        # Compose gcode command
        gcode = ("M42 P%d S255\n"
        "M42 P%d S255\n"
        "G1 F6000 X%s Y%s\n"
        "M42 P%d S0\n"
        "M42 P%d S0\n")  % (self.magnet1_pin, self.magnet2_pin, x, y, self.magnet1_pin, self.magnet2_pin)

        # Send command to ouija
        if self.magic_table.online:
            self.magic_table.send(gcode)
        else:
            raise Exception("Ouija Table is not connected!")

        return True

    def say(self, phrase):
        for character in phrase:
            self.go_to(character)
            time.sleep(1)



if __name__ == '__main__':
    ouija = OuijaController('/dev/ttyACM0','115200', 4, 5)
    ouija.connect()
    ouija.go_to('a')
    ouija.disconnect()


