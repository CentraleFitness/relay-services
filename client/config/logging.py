LOGGING_DICT = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s][%(levelname)s] %(message)s"
        }
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler"
        }
    },
    "loggers": {
        "__main__": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True
        },
        "config": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True
        },
    }
}
