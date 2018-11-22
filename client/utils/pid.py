""" Utility to run only one instance of a program """

import os
import logging
import platform
import config.config as config

if platform.system() == 'Windows':
    ### I actually have no idea how to do it on Windows
    ### I'll research that later
    class Pid:
        def __init__(self, *args):
            return None

        def is_running(self):
            return False

        def set_pidfile(self):
            pass
else:
    class Pid:
        def __init__(self, name: str):
            self.log = logging.getLogger()
            self._pid = os.getpid()
            self._file = "{}/{}.pid".format(config.PID_DIR, name)
            if config.PID_DIR != '/var/run':
                print(
                    "You are using a directory not root-friendly, "
                    "make sure that you have the correct access rights")

        def is_running(self) -> bool:
            try:
                with open(self._file, 'r') as fhandler:
                    old_pid = int(fhandler.read())
            except FileNotFoundError:
                return False
            try:
                os.kill(old_pid, 0)
            except Exception:
                return False
            return True

        def set_pidfile(self) -> None:
            try:
                if not os.path.isdir(os.path.dirname(self._file)):
                    os.makedirs(os.path.dirname(self._file))
                with open(self._file, 'w') as fhandler:
                    fhandler.write(str(self._pid))
            except Exception as ex:
                self.log.error(f"Exception handled: {ex}")

        def delete(self) -> None:
            try:
                os.remove(self._file)
            except Exception as ex:
                self.log.error(f"Exception handled: {ex}")
