"""
    Use:
        Call dict_config() to setup your logging instance
        Then, for each function, call get_logger(__name__)
"""

import time
import logging
import logging.handlers
from logging import critical, error, warning, info, debug
from logging.config import dictConfig as dict_config
from logging import getLogger as get_logger
import graypy

from config import LOGGING_DICT

dict_config(LOGGING_DICT)

SYSLOG_ADDR = ('localhost', logging.handlers.SYSLOG_UDP_PORT)
