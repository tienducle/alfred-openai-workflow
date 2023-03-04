#!/usr/bin/env python3
import os
import json
from alfred_pyutils import Logger

_CURRENT_VERSION = 1

_STORAGE_FORMAT = {
    "_version": _CURRENT_VERSION,
    "history_cache": []
}

_LOGGER = Logger(__name__)


class Storage:

    def __init__(self, storage_file_name):
        self._storage_file_name = storage_file_name
        self.__load_or_create_storage()

    def __is_storage_valid(self) -> bool:
        """
        Simple version check to invalidate storage file if it's not matching the current version.
        :return: True if storage matches the current version, False otherwise
        """
        if '_version' not in self._storage:
            _LOGGER.error('Invalid storage file.')
            return False
        return True

    def __load_or_create_storage(self):
        """
        Loads storage file or creates a new one if it doesn't exist.
        """
        with open(self._storage_file_name, encoding='utf-8') as storage_file:
            if os.path.exists(self._storage_file_name):
                try:
                    self._storage = json.loads(storage_file.read())
                    if not self.__is_storage_valid():
                        self._storage = _STORAGE_FORMAT
                except json.decoder.JSONDecodeError:
                    _LOGGER.error('Error reading storage file.')
                    pass

    def __write_storage(self):
        """
        Writes storage to file.
        """
        with open(self._storage_file_name, 'w', encoding='utf-8') as storage_file:
            storage_file.write(json.dumps(self._storage, ensure_ascii=False))

    def get(self, key):
        """
        Returns value for given key or None if it doesn't exist.
        """
        if key in self._storage:
            return self._storage[key]
        return None

    def set(self, key, value):
        """
        Sets value for given key.
        """
        self._storage[key] = value
        self.__write_storage()

    def __get_or_create_history_cache(self) -> list:
        """
        Returns history cache or creates a new empty cache if it doesn't exist.
        :return: List of history cache items
        """
        if 'history_cache' in self._storage:
            return self._storage['history_cache']
        self._storage['history_cache'] = []
        return self._storage['history_cache']

    def __get_history_cache_size(self):
        """
        Returns the size of the history cache.
        :return: Size of the history cache
        """
        return len(self.__get_or_create_history_cache())

    def add_to_history_cache(self, query, response):
        """
        Adds a new item to the history cache. If the cache is full, the first item will be removed.
        This is meant to store full Alfred responses for a given user query, so that the same query
        can be answered from the cache without needing to query an API again.
        """
        history_cache_item = {"query": query, "response": response}
        if self.__get_history_cache_size() > 5:
            _LOGGER.debug('History cache is full, removing first item..')
            self._storage['history_cache'].pop(0)
        self._storage['history_cache'].append(history_cache_item)
        self.__write_storage()

    def get_from_history_cache(self, query):
        """
        Returns the response for a given query from the history cache.
        """
        for item in self._storage['history_cache']:
            if item['query'] == query:
                return item['response']
        return None


if __name__ == '__main__':
    storage = Storage('storage.json')
    storage.set('test', 'test')
    print(storage.get('test'))
    storage.add_to_history_cache('test', 'test')
    print(storage.get_from_history_cache('test'))
