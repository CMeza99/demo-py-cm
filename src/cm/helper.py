""" Helper classes and functions
"""

import logging

_LOG = logging.getLogger(__name__)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        elif getattr(cls, "addhosts", None):
            hosts = []
            if args:
                hosts = args[0]
            hosts = kwargs.get("hosts", hosts)

            if hosts:
                _LOG.debug("Attempting to append %s to instance %s", hosts, cls)
                return cls._instances[cls].addhosts(hosts)

        return cls._instances[cls]
