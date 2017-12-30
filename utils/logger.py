import logging
from logging import critical, error, warning, info, debug
import time

from .singleton import Singleton

class Logger(object, metaclass=Singleton):
    """description of class"""

    def __init__(self, **kwargs):
        """
        Initialise a Logger class. This is a singleton so it instanciate
        only once.
        A default formatter is set for every handlers.
        A level of debug is determined by: 'critical', 'error',
        'warning', 'info', 'debug', 'notset' from the most import to the least
        """
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
        self.format = logging.Formatter(
            '[%(asctime)s][%(levelname)s] %(message)s')
        self.format.default_time_format = '%H:%M:%S'
        self.format.default_msec_format = '%s.%03d'
        return super().__init__(**kwargs)

    def __add_handler_to_basicconfig(self, handler, new_level):
        """
        Add the handler to the list of active ones and call basicConfig()
        Assertion is made when the handler is already in the list or
        the new level set does not exist
        """
        assert new_level in self.level.keys() and handler not in self.handlers
        self.handlers.append(handler)
        logging.basicConfig(handlers=self.handlers, level=self.level[new_level])

    def add_file_handler(self,  destfolder: str = "./logs/",
                         nameformat: str = "%y%m%d_%H%M%S", **kwargs):
        """
        Give a file nameformat and a folder to write logs in a file
        The nameformat goes through time.strftime()
        kwargs:
            level: update the logging level of the program
        """
        handler = logging.FileHandler(
            "{}/{}.log".format(destfolder, time.strftime(nameformat)))
        handler.setFormatter(self.format)
        self.__add_handler_to_basicconfig(
            handler, kwargs.get('level', self.curr))

    def add_stream_handler(self, stream, **kwargs):
        """
        Add a stream to output the logs
        kwargs:
            level: update the logging level of the program
        """
        handler = logging.StreamHandler(stream)
        handler.setFormatter(self.format)
        self.__add_handler_to_basicconfig(
            handler, kwargs.get('level', self.curr))

    def add_udp_handler(self, host):
        # TODO
        pass