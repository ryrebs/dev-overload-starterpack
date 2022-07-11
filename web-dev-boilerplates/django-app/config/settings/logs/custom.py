recs = set()


def filter_duplicate(record):
    """
    Sample custom filter func.
    Return False if lineno should
    not be added to record, otherwise return True.
    """
    if record.lineno in recs:
        return False
    else:
        recs.add(record.lineno)
        return True


LOGGING = {
    "version": 1,
    ## We still want django existing loggers
    ## to avoid creating loggers for each modules.
    ## We only create new loggers for each module
    ## as necessary.
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "custom_filter_duplicate": {
            "()": "django.utils.log.CallbackFilter",
            "callback": filter_duplicate,
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    ## Handlers determine how each log is processed.
    "handlers": {
        "console_verbose": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "production_handler": {
            "level": "WARNING",
            "filters": [
                "require_debug_false",
            ],
            "class": "logging.handlers.RotatingFileHandler",  # set maxsize(bytes), backup count
            "filename": "logs/django/django_production.log",  # path to log folder, should be writeable
            "maxBytes": 1024 * 1024 * 100,  # 100MB
            "backupCount": 5,
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    ## Create/Override the loggers.
    "loggers": {
        ## name returned by logging.getLogger
        "appname.module": {
            "handlers": [
                "production_handler",
            ],
            "filters": [
                "require_debug_false",
            ],
            ## Set lowest log level to DEBUG
            ## and filtered by the handlers log level.
            "level": "INFO",
        },
        "django": {
            "handlers": [
                "production_handler",
                "mail_admins",
            ],
            "level": "DEBUG",
        },
        "django.security": {
            ## Send security logs to admin.
            "handlers": [
                "mail_admins",
            ],
            "level": "ERROR",
            "propagate": False,
        },
        "py.warnings": {
            ## Log warnings on console during dev
            ## and production for unforseen warnings.
            "handlers": [
                "console",
                "production_handler",
            ],
            "level": "DEBUG",
        },
    },
}
