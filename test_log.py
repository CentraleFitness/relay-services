import sys
import logging

if __name__ == "__main__":
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
    formatter.default_time_format = '%H:%M:%S'
    formatter.default_msec_format = '%s.%03d'
    sh.setFormatter(formatter)
    logging.basicConfig(
        handlers=(sh, ),
        level=logging.DEBUG)
    logging.debug('test')

