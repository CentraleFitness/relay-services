import sys
import time
import logging
from collections import defaultdict
import argparse


from config import *
from utils.thread import *
import utils.logger as logger
from hardware.oled_128_64 import *
from hardware.joystick import Joystick
from hardware.pushbutton import Pushbutton, PBStatus
from objects.graphics.gtextbox import *
from objects.graphics.gcontainer import GContainer
from utils.pid import Pid


def input_controller(t_id, t_controller, input):
    ilogger = logging.getLogger('oled.input')
    ilogger.debug("Thread {}: started".format(t_id))
    if isinstance(input, Joystick):
        ilogger.debug("Listening: Joystick")
        while t_controller[t_id] == ThreadStatus.RUNNING:
            for entry in input.get_inputs():
                t_controller.queue.put(entry)
            time.sleep(.05)
    elif isinstance(input, Pushbutton):
        ilogger.debug("Listening: Button")
        while t_controller[t_id] == ThreadStatus.RUNNING:
            mem = input.get_status_update()
            if mem:
                t_controller.queue.put(mem)
            time.sleep(.05)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="hotspot.py",
                                     description="Start the bluetooth server")
    parser.add_argument('--silent', dest="log_stdout", action='store_false')
    local_log = parser.add_mutually_exclusive_group()
    local_log.add_argument('--no-local-log',
                           dest="log_folder",
                           action='store_const',
                           const=None,
                           help='Disable the local trace of logs')
    local_log.add_argument('-local-log',
                           dest="log_folder",
                           type=str,
                           help='Defines the folder where the lof trace goes')
    udp_log = parser.add_mutually_exclusive_group()
    udp_log.add_argument('--no-udp-log',
                         dest="log_udp",
                         action='store_false')
    udp_log.add_argument('-udp-log',
                         dest="udp_host",
                         type=str,
                         nargs=2,
                         metavar=('ip', 'port'))
    args = parser.parse_args(sys.argv[1:])

    log = logger.Logger(level='debug')
    log.add_file_handler()
    log.add_stream_handler(sys.stdout)

    onetime_program = Pid('oled')
    if onetime_program.is_running():
        logger.error('Program is already running')
        sys.exit(1)
    else:
        onetime_program.set_pidfile()
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
        logger.debug('Ctrl-c pressed')
        c.stop_all()
        logger.info('Program terminated')
