import logging
from .singleton import Singleton

class Logger(object, metaclass=Singleton):
    """description of class"""

    def __init__(self, **kwargs):
        level = {
            'critical': logging.CRITICAL,
            'error': logging.ERROR,
            'warning': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG,
            'notset': logging.NOTSET
            }
        self.log = logging.getLogger('oled')
        self.log.setLevel(level.get(kwargs.get('level', 'debug')))
        self.format = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
        self.format.default_time_format = '%H:%M:%S'
        self.format.default_msec_format = '%s.%03d'
        return super().__init__(**kwargs)

    def add_file_handler(self, nameformat: str = "%y%m%d_%H%M%S",
                         destfolder: str = "./logs/"):
        """The nameformat goes through time.strftime()"""
        handler = logging.FileHandler(
            "{}/{}.log".format(destfolder, nameformat))
        handler.setFormatter(self.format)
        self.log.addHandler(handler)

    def add_stream_handler(self, stream):
        handler = logging.StreamHandler(stream)
        handler.setFormatter(self.format)
        self.logger.addHandler(handler)

    def add_udp_handler(self, host):
        # TODO
        pass