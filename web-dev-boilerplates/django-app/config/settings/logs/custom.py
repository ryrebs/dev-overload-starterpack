recs = set()


def filter_duplicate(record):
    if record.lineno in recs:
        return False
    else:
        recs.add(record.lineno)
        return True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    # format of logs
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
    # when should a log be recorded
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
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "development_handler": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/django/django_development.log",  # path to log folder, should be writeable
            "maxBytes": 1024 * 1024 * 100,  # 100MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "production_handler": {
            "level": "INFO",
            "filters": [
                "require_debug_false",
                "custom_filter_duplicate",
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
    "loggers": {
        "django": {
            "handlers": [
                "console",
                "production_handler",
                "development_handler",
                "mail_admins",
            ],
        },
        "django.security": {
            "handlers": [
                "mail_admins",
            ],
            "level": "ERROR",
            "propagate": False,
        },
        "py.warnings": {
            "handlers": [
                "console",
                "production_handler",
                "development_handler",
            ],
        },
    },
}
