##      General             ##
SERVER_IP = ''

##      API Connection      ##
API_PORT = 0
API_KEY = ''
API_URL = "http://{ip}:{port}/".format(ip=SERVER_IP, port=API_PORT)

##      Logging             ##
GELF_INPUT_PORT = 5544
LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
            },
        'graypy': {
            'level': 'DEBUG',
            'class': 'graypy.GELFHandler',
            'host': SERVER_IP,
            'port': GELF_INPUT_PORT,
            },
        },
    'loggers': {
        '__main__': {
            'handlers': ['graypy', 'console'],
            'level': 'DEBUG',
            'propagate': True
            },
        'network': {
            'handlers': ['graypy', 'console'],
            'level': 'DEBUG',
            'propagate': True
            }
        }
    
    }
