from .pushbutton import Pushbutton

class Joystick(object):
    """A Joystick"""

    def __init__(self, *args, **kwargs):
        self.pbuttons = (
            Pushbutton('L', 27),
            Pushbutton('R', 23),
            Pushbutton('C', 4),
            Pushbutton('U', 17),
            Pushbutton('D', 22)
            )
        self.description = kwargs.get('description', "")

    def get_inputs(self) -> list:
        inputs = list()
        for pbutton in self.pbuttons:
            mem = pbutton.get_status_update()
            if mem:
                inputs.append(mem)
        return inputs
