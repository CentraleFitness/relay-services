import time

from hardware.oled_128_64 import *
from hardware.joystick import Joystick, Pushbutton
from objects.graphics.gtextbox import *
from objects.graphics.gcontainer import GContainer


if __name__ == "__main__":
    joy1 = Joystick()
    a_button = Pushbutton('A', 5)
    b_button = Pushbutton('B', 6)

    while True:
        print(joy1.get_inputs())
        print(a_button.get_status_update())
        print(b_button.get_status_update())
        time.sleep(.1)                    
    display = Oled_128_64(
        content=GContainer(
            SCREEN_SIZE,
            (0, 0),
            objects=[
                GTextBox((100, 9), (0, 0), "Toto", x=1, y=-1),
                GTextBox((100, 9), (0, 9), "Tata", x=1, y=-1),
                GTextBox((100, 9), (0, 18), "Titi", x=1, y=-1)
                ]))
    display.update_content()
    display.display_content()
