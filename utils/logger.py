import logging
import time
from .singleton import Singleton

class Logger(object, metaclass=Singleton):
    """description of class"""

    def __init__(self, **kwargs):
        self.level = {
            'critical': logging.CRITICAL,
            'error': logging.ERROR,
            'warning': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG,
            'notset': logging.NOTSET
            }
        self.curr = kwargs.get('level', 'debug')
        self.handlers = list()
        #self.log = logging.getLogger('oled')
        #self.log.setLevel(level.get(kwargs.get('level', 'debug')))
        self.format = logging.Formatter(
            '[%(asctime)s][%(levelname)s] %(message)s')
        self.format.default_time_format = '%H:%M:%S'
        self.format.default_msec_format = '%s.%03d'
        return super().__init__(**kwargs)

    def __add_handler_to_basicconfig(self, handler, new_level):
        self.handlers.append(handler)
        try:
            logging.basicConfig(handlers=self.handlers, level=self.level[new_level])
        except Exception:
            # DO something

    def add_file_handler(self, nameformat: str = "%y%m%d_%H%M%S",
                         destfolder: str = "./logs/", **kwargs):
        """
        Give a file nameformat and a folder to write logs in a file
        The nameformat goes through time.strftime()
        kwargs:
            level: update the logging level of the program
        """
        handler = logging.FileHandler(
            "{}/{}.log".format(destfolder, time.strftime(nameformat)))
        handler.setFormatter(self.format)
        #self.log.addHandler(handler)
        self.__add_handler_to_basicconfig(handler, kwargs.get('level', self.curr))
        self.handlers.append(handler)
        logging.basicConfig(handlers=self.handlers, level=self.level[self.curr])


    def add_stream_handler(self, stream):
        handler = logging.StreamHandler(stream)
        handler.setFormatter(self.format)
        #self.logger.addHandler(handler)

    def add_udp_handler(self, host):
        # TODO
        pass