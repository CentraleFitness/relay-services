import time
import concurrent.futures
from collections import defaultdict
from enum import Enum
from queue import Queue


#if platform.system() == "Windows":
#    print("Program running on windows")
#else:

from hardware.oled_128_64 import *
from hardware.joystick import Joystick
from hardware.pushbutton import Pushbutton, PBStatus
from objects.graphics.gtextbox import *
from objects.graphics.gcontainer import GContainer

class ThreadStatus(Enum):
    STOPPED = 0
    RUNNING = 1

class ThreadController():
    def __init__(self, *args, **kwargs):
        self.workers = kwargs.get('max_workers', 3)
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.workers)
        self.futures = dict()
        self.status = dict()
        self.queue = Queue()
        self.last_thread_id = 0x00

    def _get_id(self):
        self.last_thread_id += 1
        return self.last_thread_id - 1

    def start(self, func, *args, **kwargs):
        if isinstance(kwargs.get('chain', None), (list, tuple)):
            for t_args in kwargs['chain']:                   
                id = self._get_id()
                self.futures[id] = self.executor.submit(id, *t_args)
                self.status[id] = ThreadStatus.RUNNING
        else:
            id = self._get_id()
            self.futures[id] = self.executor.submit(func, id, *args)
            self.status[id] = ThreadStatus.RUNNING

    def stop(self, thread_id):
        self.status[thread_id] = ThreadStatus.STOPPED

    def stop_all(self):
        for thread in self.status:
            self.status[thread] = ThreadStatus.STOPPED


def input_controller(input, queue, controller):
    print("Thread started", flush=True)
    if isinstance(input, Joystick):
        while controller.running:
            for entry in input.get_inputs():
                queue.put(entry)
            time.sleep(.05)
    elif isinstance(input, Pushbutton):
        while controller.running:
            mem = input.get_status_update()
            if mem:
                queue.put(mem)
            time.sleep(.05)
    

if __name__ == "__main__":
    joy1 = Joystick()
    a_button = Pushbutton('A', 5)
    b_button = Pushbutton('B', 6)

    display = Oled_128_64(content=None)
    menu2 = GContainer(
        SCREEN_SIZE,
        (0, 0),
        objects=[
            GTextBox((110, 9), (0, 0), "Broadcasting...", x=1, y=-1),
            GTextBox((110, 9), (0, 9), "Found:", x=1, y=-1),
            GTextBox((110, 9), (10, 18), "cf-relay-001", x=1, y=-1),
            GTextBox((110, 9), (10, 27), "cf-relay-004", x=1, y=-1)
        ])
    menu3 = GContainer(
        SCREEN_SIZE,
        (0, 0),
        objects=[
            GTextBox((110, 9), (0, 0), "Connection status:", x=1, y=-1),
            GTextBox((110, 9), (10, 9), "server: OK", x=1, y=-1),
            GTextBox((110, 9), (10, 18), "active relay: 3", x=1, y=-1)
        ])
    menu4 = GContainer(
        SCREEN_SIZE,
        (0, 0),
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

    c = ThreadController()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        tasks = [
            executor.submit(input_controller, controller, awaiting_input, c) \
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
                print(time.time() - start)
        except KeyboardInterrupt:
            print(" Killin' the fun")
            c.running = False
