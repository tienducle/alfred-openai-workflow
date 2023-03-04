#!/usr/bin/env python3
from alfred_pyutils import Logger

_LOGGER = Logger(__name__)


class StrUtils:

    @staticmethod
    def get_clean_text(item):
        text = ''
        if 'text' in item:
            text = item['text']
        if 'message' in item:
            text = item['message']['content']

        completed_pre_processing = False
        while not completed_pre_processing:
            #_LOGGER.debug('Cleaning up text: ' + text)
            old_length = len(text)
            text = text.strip('?').strip(',').strip()
            if len(text) == old_length:
                completed_pre_processing = True
                #_LOGGER.debug('Returning clean text: ' + text)
        return text
