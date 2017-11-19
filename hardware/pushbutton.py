
class Pushbutton(object):
    """Pushbutton responding to a GPIO on the Raspberry Pi"""

    def __init__(self, pin: int):
        self.pin = pin
        self.action = None
        self.description = None
