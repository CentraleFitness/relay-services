#import sys
#import logging

#if __name__ == "__main__":
#    sh = logging.StreamHandler(sys.stdout)
#    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
#    formatter.default_time_format = '%H:%M:%S'
#    formatter.default_msec_format = '%s.%03d'
#    sh.setFormatter(formatter)
#    logging.basicConfig(
#        handlers=(sh, ),
#        level=logging.DEBUG)
#    logging.debug('test')

import sys
import utils.logger as logger

if __name__ == "__main__":
    log = logger.Logger()
    #log.add_file_handler('test', './logs/')
    log.add_stream_handler(sys.stdout)
    log.add_udp_handler('127.0.1.1', 5544)
    logger.debug('test')
