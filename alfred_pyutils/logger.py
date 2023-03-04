#!/usr/bin/env python3
import logging


class Logger:
    def __init__(self, module_name):
        console = logging.StreamHandler()
        # '%(asctime)s %(filename)s:%(lineno)s'
        fmt = logging.Formatter(
            '%(asctime)s ' + module_name + ' %(levelname)-8s %(message)s',
            datefmt='%H:%M:%S')
        console.setFormatter(fmt)

        self._logger = logging.getLogger('alfred-workflow-' + module_name)
        self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(console)

    def debug(self, message):
        self._logger.debug(message)

    def info(self, message):
        self._logger.info(message)

    def error(self, message):
        self._logger.error(message)
