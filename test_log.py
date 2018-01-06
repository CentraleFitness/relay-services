#import sys
#import logging
import time

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
    log.level = 'debug'
    log.add_stream_handler(sys.stdout)
    log.add_syslog_handler('/dev/log')
    log.set_config()
    try:
        logger.critical("critical log")
        logger.error("error log")
        logger.warning("warning log")
        logger.info("info log")
        logger.debug("debug log")
        for i in range(100):
            time.sleep(1)
            logger.debug(i)
    except KeyboardInterrupt:
        logger.warning('execution stopped')
