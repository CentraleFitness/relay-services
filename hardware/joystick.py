from .pushbutton import Pushbutton

class Joystick(object):
    """A Joystick"""

    def __init__(self, *args, **kwargs):
        self.pbuttons = (
            Pushbutton('L_pin', 27),
            Pushbutton('R_pin', 23),
            Pushbutton('C_pin', 4),
            Pushbutton('U_pin', 17),
            Pushbutton('D_pin', 22)
            )
        self.description = kwargs.get('description', "")

    def get_inputs(self) -> list:
        inputs = list()
        for pbutton in self.pbuttons:
            mem = pbutton.get_status_update()
            if mem:
                inputs.append(mem)
        return inputs
