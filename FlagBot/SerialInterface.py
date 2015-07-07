"""
    SerialInterface.py
    --------------------------------------
    Controls a servo by sending commands through a serial port
"""

__author__ = "def"
__licence__ = "GPLv3"

import serial

class SerialInterface:

    def __init__(self):
        self.serialPort = None


    def connect(self, port, baudrate):
        """
        Connect with the serial port at a certain baudrate
        """
        # Setup serial port
        self.serialPort = serial.Serial()
        self.serialPort.port = port
        self.serialPort.baudrate = baudrate

        # Open port
        self.serialPort.open()

        if not self.serialPort.isOpen():
            raise IOError("Port could not be opened!")



    def sendPing(self):
        """
        Sends ping signal through the serial port
        """
        try:
            self.serialPort.write('PING\n')
        except AttributeError, e:
            print 'Not connected: [' + str(e) + ']'


    def sendMove(self, pos):
        """
        Sends the command to move the servo to pos
        """
        if 0 <= pos <= 180:
            command = "M%d\n" % pos
        else:
            raise Exception('Position value %d out of range [0, 180]'%pos)

        try:
            self.serialPort.write(command)
        except AttributeError, e:
            print 'Not connected: [' + str(e) + ']'


    def sendToggle(self):
        """
        Sends the command to toggle the LED
        """
        try:
            self.serialPort.write('L\n')
        except AttributeError, e:
            print 'Not connected: [' + str(e) + ']'



# If the script is run directly, this example is executed:
if __name__ == "__main__":
    import time as t

    interface = SerialInterface()
    interface.connect("/dev/ttyUSB0", 9600)

    interface.sendPing()
    interface.sendToggle()
    t.sleep(5)
    interface.sendMove(0)
    t.sleep(5)
    interface.sendMove(180)
    t.sleep(5)
    interface.sendMove(0)