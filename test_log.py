#import sys
#import logging
import time
import logging.handlers

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
    log.add_udp_handler('192.168.254.35', 5544)
    try:
        logging.critical("critical log")
        logging.error("error log")
        logging.warning("warning log")
        logging.info("info log")
        logging.debug("debug log")
        for i in range(10):
            time.sleep(1)
            logger.debug(i)
    except KeyboardInterrupt:
        logger.warning('execution stopped')
