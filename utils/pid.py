""" Utility to run only one instance of a program """

import os

PID_DIR = "/var/run"

class Pid:
    def __init__(self, name: str):
        self._pid = os.getpid()
        self._file = "{}/{}.pid".format(PID_DIR, name)

    def is_running(self):
        try:
            with open(self._file, 'r') as file:
                old_pid = int(file.read())
        except FileNotFoundError:
            return False
        try:
            os.kill(old_pid, 0)
        except Exception:
            return False
        return True

    def set_pidfile(self):
        with open(self._file, 'w') as file:
            file.write(str(self._pid))
        
