import time

from hardware.oled_128_64 import *
from hardware.joystick import Joystick
from hardware.pushbutton import Pushbutton, PBStatus
from objects.graphics.gtextbox import *
from objects.graphics.gcontainer import GContainer


if __name__ == "__main__":
    joy1 = Joystick()
    a_button = Pushbutton('A', 5)
    b_button = Pushbutton('B', 6)

    menu1 = GContainer(
        SCREEN_SIZE,
        (0, 0),
        objects=[
            GTextBox((100, 9), (0, 0), "Toto", x=1, y=-1),
            GTextBox((100, 9), (0, 9), "Tata", x=1, y=-1),
            GTextBox((100, 9), (0, 18), "Titi", x=1, y=-1)
        ])
    display = Oled_128_64(content=menu1)
    cursor = 0
    menu1.objects[cursor % len(menu1.objects)].selected = True
    display.update_content()
    display.display_content()
    try:
        while True:
            tmp = joy1.get_inputs()
            if ('U_pin', PBStatus.RELEASED) in tmp:
                menu1.objects[cursor % len(menu1.objects)].selected = False
                cursor -= 1
                menu1.objects[cursor % len(menu1.objects)].selected = True
                display.update_content()
                display.display_content()
            elif ('D_pin', PBStatus.RELEASED) in tmp:
                menu1.objects[cursor % len(menu1.objects)].selected = False
                cursor += 1
                menu1.objects[cursor % len(menu1.objects)].selected = True
                display.update_content()
                display.display_content()
    except KeyboardInterrupt:
        print("Ctrl-C")
