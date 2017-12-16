import sys
import time
import concurrent.futures

import logging

from collections import defaultdict
from enum import Enum
from queue import Queue
from hardware.oled_128_64 import *
from hardware.joystick import Joystick
from hardware.pushbutton import Pushbutton, PBStatus
from objects.graphics.gtextbox import *
from objects.graphics.gcontainer import GContainer

from pid.pid import Pid

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

    def __getitem__(self, item):
        return self.status[item]

    def _get_id(self):
        self.last_thread_id += 1
        return self.last_thread_id - 1

    def start(self, func, *args, **kwargs):
        if isinstance(kwargs.get('factory', None), (list, tuple)):
            for t_args in kwargs['factory']:                   
                id = self._get_id()
                self.futures[id] = self.executor.submit(func, id, self, *t_args)
                self.status[id] = ThreadStatus.RUNNING
        else:
            id = self._get_id()
            self.futures[id] = self.executor.submit(func, id, self, *args)
            self.status[id] = ThreadStatus.RUNNING

    def stop(self, thread_id):
        self.status[thread_id] = ThreadStatus.STOPPED

    def stop_all(self):
        for thread in self.status:
            self.status[thread] = ThreadStatus.STOPPED


def input_controller(t_id, t_controller, input):
    print("Thread started", flush=True) #DEBUG // SYSLOG
    if isinstance(input, Joystick):
        while t_controller[t_id] == ThreadStatus.RUNNING:
            for entry in input.get_inputs():
                t_controller.queue.put(entry)
            time.sleep(.05)
    elif isinstance(input, Pushbutton):
        while t_controller[t_id] == ThreadStatus.RUNNING:
            mem = input.get_status_update()
            if mem:
                t_controller.queue.put(mem)
            time.sleep(.05)
    

    

if __name__ == "__main__":

    logger = logging.getLogger('oled')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('test.log')
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
            
    onetime_program = Pid('oled')
    if onetime_program.is_running():
        logger.error('Program is already running')
        sys.exit()
    else:
        logger.info('Program is starting')

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

    c = ThreadController(max_workers=3)
    c.start(input_controller, factory=
            ((joy1, ),
             (a_button, ),
             (b_button, )))    
    try:
        while True:
            while not c.queue.empty():
                input = c.queue.get()
                if input[1] == PBStatus.RELEASED:
                    display.interact(input[0])
                c.queue.task_done()

            display.update_content()
            display.display_content()
    except KeyboardInterrupt:
        print(" Killin' the fun")
        c.stop_all()
        logger.info('Program terminated')
