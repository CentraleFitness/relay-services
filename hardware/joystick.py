
class Joystick(object):
    """A Joystick"""

    def __init__(self, pin: int):
        self.pin = pin
        self.action = {
            'UP': None,
            'DOWN': None,
            'LEFT': None,
            'RIGHT': None,
            'PUSH': None
            }
        self.description = None
