#!/usr/bin/env python3
import json
import requests
from alfred_pyutils import Logger

_BASE_URL = 'https://api.openai.com/v1'
_LOGGER = Logger(__name__)


class OpenAiClient:
    def __init__(self, auth_token: str, model_text_completion: str, model_chat_completion: str, max_tokens: int,
                 max_completions: int) -> None:
        self._auth_token = auth_token
        self._model_text_completion = model_text_completion
        self._model_chat_completion = model_chat_completion
        self._max_tokens = int(max_tokens)
        self._max_completions = int(max_completions)

    def get_chat_completion(self, query: str) -> object:
        """
        Sends the query in a Chat Completion request to /chat/completions and returns the response as object.
        """
        _LOGGER.debug('Requesting chat completion..')
        url = _BASE_URL + '/chat/completions'
        data = {
            'model': self._model_chat_completion,
            'max_tokens': self._max_tokens,
            'n': self._max_completions,
            'messages': [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
        return self.__post(url, data)

    def get_text_completion(self, query: str) -> object:
        """
        Sends the query in a Text Completion request to /completions and returns the response as object.
        """
        _LOGGER.debug('Requesting text completion..')
        url = _BASE_URL + '/completions'
        data = {
            'model': self._model_text_completion,
            'max_tokens': self._max_tokens,
            'n': self._max_completions,
            'prompt': query
        }
        return self.__post(url, data)

    def get_image_completion(self, query: str) -> object:
        """
        Sends the query in an Image Completion request to /images/generations and returns the response as object.
        """
        _LOGGER.debug('Requesting image generation..')
        url = _BASE_URL + '/images/generations'
        data = {
            'size': '1024x1024',
            'n': self._max_completions,
            'response_format': 'url',
            'prompt': query
        }
        return self.__post(url, data)

    def __post(self, url: str, data: object) -> object:
        """
        Sends a POST request to the given url with the given data and returns the response as object.
        """
        response = requests.post(url,
                                 auth=('', self._auth_token),
                                 json=data)
        response_body_json = response.text
        _LOGGER.debug(response_body_json)
        return json.loads(response_body_json)
