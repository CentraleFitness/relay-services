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
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        ###
        self.name = name
        self.pin = pin
        self.action = kwargs.get('action', None)
        self.description = kwargs.get('description', "")
        self.status = PBStatus.RELEASED

    def _update_status(self) -> None:
        if not GPIO.input(self.pin) and self.status == PBStatus.RELEASED:
            self.status = PBStatus.PRESSED
        elif GPIO.input(self.pin) and self.status == PBStatus.PRESSED:
            self.status = PBStatus.RELEASED

    def get_status_update(self):
        if not GPIO.input(self.pin) and self.status == PBStatus.RELEASED:
            self.status = PBStatus.PRESSED
            return (self.name, self.status)
        elif GPIO.input(self.pin) and self.status == PBStatus.PRESSED:
            self.status = PBStatus.RELEASED
            return (self.name, self.status)
        return None

    def status(self, force_update=False) -> tuple:
        if force_update:
            self._update_status()
        return (self.name, self.status)
