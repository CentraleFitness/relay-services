import sys
import subprocess
import socketserver
import threading

from oled.oled import Oled
from pid.pid import Pid


class CommandUDPHandler(socketserver.BaseRequestHandler):
    def setup(self):
        pass

    def handle(self):
        data = self.request[0].strip()
        print("{}: {}".format(self.client_address[0], data))
        fptr, param = self.parse(data)
        if fptr:
            fptr(param)

    def finish(self):
        display.refresh()

    def parse(self, msg: bytes) -> tuple:
        command = msg.decode("utf-8").split(':', maxsplit=1)
        if command[0] == "write":
            fptr = display.add_line
            param = command[1]
        elif command[0] == "clear":
            if command[1] == "all":
                fptr = display.delete_all_lines
                param = None
            elif command[1].count('-') == 1:
                fptr = display.delete_line_range
                param = [int(i) for i in command[1].split('-')]
            else:
                fptr = display.delete_line
                param = [int(i) for i in command[1].split(',')]
        elif command[0] == "stop" and command[1] == "now":
            fptr = self.stop_server()
            param = None
        return fptr, param

    def stop_server(self, *args):
        threading.Thread(target=self.server.shutdown).start()


if __name__ == "__main__":
    display = Oled()
    display.clear_screen()
    display.refresh()
    display.add_line(
        "Boot " + subprocess.check_output(
            "date '+%D %R'", shell=True).decode("utf-8"))
    display.add_line(
        "IP " + subprocess.check_output(
            "hostname -I", shell=True).decode("utf-8"))
    display.refresh()

    my_pid = Pid("oled")
    assert not my_pid.is_running()
    my_pid.set_pidfile()
    server = socketserver.UDPServer(('127.0.1.1', 4000), CommandUDPHandler)
    server.serve_forever()

    # When the server is stopped
    display.clear_screen()
