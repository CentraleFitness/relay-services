import time


#if platform.system() == "Windows":
#    print("Program running on windows")
#else:

from hardware.oled_128_64 import *
from hardware.joystick import Joystick
from hardware.pushbutton import Pushbutton, PBStatus
from objects.graphics.gtextbox import *
from objects.graphics.gcontainer import GContainer


if __name__ == "__main__":
    joy1 = Joystick()
    a_button = Pushbutton('A', 5)
    b_button = Pushbutton('B', 6)

    display = Oled_128_64(content=None)
    menu2 = GContainer(
        SCREEN_SIZE,
        (0, 0),
        #parent=menu1,
        objects=[
            GTextBox((110, 9), (0, 0), "Broadcasting...", x=1, y=-1),
            GTextBox((110, 9), (0, 9), "Found:", x=1, y=-1),
            GTextBox((110, 9), (10, 18), "cf-relay-001", x=1, y=-1),
            GTextBox((110, 9), (10, 27), "cf-relay-004", x=1, y=-1)
        ])
    menu3 = GContainer(
        SCREEN_SIZE,
        (0, 0),
        #parent=menu1,
        objects=[
            GTextBox((110, 9), (0, 0), "Connection status:", x=1, y=-1),
            GTextBox((110, 9), (10, 9), "server: OK", x=1, y=-1),
            GTextBox((110, 9), (10, 18), "active relay: 3", x=1, y=-1)
        ])
    menu4 = GContainer(
        SCREEN_SIZE,
        (0, 0),
        #parent=menu1,
        objects=[
            GTextBox((110, 9), (0, 0), "System info:", x=1, y=-1),
            GTextBox((110, 9), (10, 9), "Active since 6:00", x=1, y=-1),
            GTextBox((110, 9), (10, 18), "IP 127.0.1.1", x=1, y=-1),
        ])

    menu1 = GContainer(
        SCREEN_SIZE,
        (0, 0),
        objects=[
            GTextBox((110, 9), (0, 0), "Broadcast", x=1, y=-1,
                     action=(display._change_content, menu2)),
            GTextBox((110, 9), (0, 9), "Connection status", x=1, y=-1,
                     action=(display._change_content, menu3)),
            GTextBox((110, 9), (0, 18), "System info", x=1, y=-1,
                     action=(display._change_content, menu4))
        ])

    menu2.parent = menu1
    menu3.parent = menu1
    menu4.parent = menu1

    display.content = menu1

    try:
        while True:
            tmp = joy1.get_inputs()
            tmp.append(a_button.get_status_update())
            tmp.append(b_button.get_status_update())
            for input in tmp:
                if PBStatus.RELEASED in input:
                    display.interact(input[0])
            #if ('U', PBStatus.RELEASED) in tmp:
            #    menu1.cursor.prev()
            #    display.update_content()
            #    display.display_content()
            #elif ('D', PBStatus.RELEASED) in tmp:
            #    menu1.cursor.next()
            #    display.update_content()
            #    display.display_content()
            #if a_button.get_status_update() == ('A', PBStatus.RELEASED):
            #    display.content = menus[cursor % len(menu1.objects)]
            #    display.update_content()
            #    display.display_content()
            #elif b_button.get_status_update() == ('B', PBStatus.RELEASED):
            #    display.content = menu1
            #    display.update_content()
            #    display.display_content()
            display.update_content()
            display.display_content()
    except KeyboardInterrupt:
        print(" Killing the fun")
