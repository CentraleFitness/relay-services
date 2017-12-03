import time
import concurrent.futures
from collections import defaultdict
from queue import Queue


#if platform.system() == "Windows":
#    print("Program running on windows")
#else:

from hardware.oled_128_64 import *
from hardware.joystick import Joystick
from hardware.pushbutton import Pushbutton, PBStatus
from objects.graphics.gtextbox import *
from objects.graphics.gcontainer import GContainer


def input_controller(input, queue):
    while True:
        if isinstance(input, Joystick):
            for entry in input.get_input():
                queue.put(entry)
        elif isinstance(input, Pushbutton):
            mem = input.get_status_update()
            if mem:
                queue.put(mem)


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
                     action=defaultdict(
                         tuple,
                         {'A': (display._change_content, menu2)})),
            GTextBox((110, 9), (0, 9), "Connection status", x=1, y=-1,
                     action=defaultdict(
                         tuple,
                         {'A': (display._change_content, menu3)})),
            GTextBox((110, 9), (0, 18), "System info", x=1, y=-1,
                     action=defaultdict(
                         tuple,
                         {'A': (display._change_content, menu4)})),
        ])

    menu2.parent = menu1
    menu3.parent = menu1
    menu4.parent = menu1

    display.content = menu1

    awaiting_input = Queue()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        tasks = [
            executor.submit(controller, awaiting_input) \
                for controller in (joy1, a_button, b_button)
            ]
        try:
            while True:
                start = time.time()

                while not awaiting_input.empty():
                    input = awaiting_input.get()
                    if input[1] == PBStatus.RELEASED:
                        display.interact(input[0])
                    awaiting_input.task_done()

                display.update_content()
                display.display_content()
                print("Loop duration: {}s".format(time.time() - start))
        except KeyboardInterrupt:
            print(" Killing the fun")
