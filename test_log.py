import sys
import time
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
