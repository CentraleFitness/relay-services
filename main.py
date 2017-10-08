import sys
import subprocess
import socketserver

from oled.oled import Oled
from pid.pid import Pid

FOR_EVER_AND_EVER = True



class CommandUDPHandler(socketserver.BaseRequestHandler):
    def setup(self):
        pass
    
    def handle(self):
        data = self.request[0].strip()
        print("{}: {}".format(self.client_address[0], data))
        fptr, param = parse(data)
        fptr(param)
        
    def finish(self):
        display.refresh()


def parse(msg: bytes):
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
    return fptr, param
            
        
def main():
    server = socketserver.UDPServer(('127.0.1.1', 4000), CommandUDPHandler)
    print("Server memory address: {}".format(server))
    server.serve_forever()

if __name__ == "__main__":
    display = Oled()
    display.clear_screen()
    display.refresh()

    if len(sys.argv) > 1 and sys.argv[1] == "stop":
        sys.exit()

    display.add_line(
        "Boot " + subprocess.check_output(
            "date '+%D %R'", shell=True).decode("utf-8"))
    display.refresh()

    my_pid = Pid("oled")
    assert not my_pid.get_is_running()
    my_pid.set_pidfile()
    main()
