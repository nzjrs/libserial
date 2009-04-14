import gobject
import os.path
import serial
import logging

LOG = logging.getLogger('libserial.SerialSender')

class SerialSender(gobject.GObject):

    __gsignals__ = {
        "serial-connected" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_BOOLEAN]),     #True if successfully connected to the port
        }

    def __init__(self, port="/dev/null", speed=9600, timeout=1):
        gobject.GObject.__init__(self)
        self._serial = None
        self._port = port
        self._speed = speed
        self._timeout = timeout
        self._opened = False

    def get_serial(self):
        return self._serial

    def is_open(self):
        return self._opened

    def connect_to_port(self, port=None, speed=None):
        """
        Opens the port
        """
        if port: p = port
        else: p = self._port
        if speed: s = speed
        else: s = self._speed

        #no-op if same port and speed is selected
        if (self._opened == False) or (s != self._speed) or (p != self._port):
            LOG.debug("Opening Port: %s @ %d" % (p,s))
            if self._serial and self._serial.isOpen():
                self._serial.close()
            try:
                self._serial = serial.Serial(p, s, timeout=self._timeout)
                self._serial.flushInput()
                self._port = p
                self._speed = s
                self._opened = self._serial.isOpen()
            except serial.SerialException:
                self._opened = False

        self.emit("serial-connected", self._opened)
        return self._opened

    def disconnect_from_port(self):
        if self._opened:
            self._serial.close()
            self._opened = False

    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        raise NotImplementedError

