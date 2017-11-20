from enum import Enum
import RPi.GPIO as GPIO

class PBStatus(Enum):
    PRESSED = 0
    RELEASED = 1

class Pushbutton(object):
    """Pushbutton responding to a GPIO on the Raspberry Pi"""

    def __init__(self, name: str, pin: int, **kwargs):
        ### Hardware setup
        if GPIO.getmode() in (GPIO.BOARD, None):
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUP_UP)
        ###
        self.name = name
        self.pin = pin
        self.action = kwargs.get('action', None)
        self.description = kwargs.get('description', "")
        self.status = PBStatus.IDLE

    def get_status_update(self):
        if not GPIO.input(self.pin) and self.status == PBStatus.RELEASED:
            self.status = PBStatus.PRESSED
            return (self.name, self.status)
        elif GPIO.input(self.pin) and self.status == PBStatus.PRESSED:
            self.status = PBStatus.PRESSED
            return (self.name, self.status)
        return None

    def get_status(self):
        if not GPIO.input(self.pin) and self.status == PBStatus.RELEASED:
            self.status = PBStatus.PRESSED
        elif GPIO.input(self.pin) and self.status == PBStatus.PRESSED:
            self.status = PBStatus.PRESSED
        return self.status
