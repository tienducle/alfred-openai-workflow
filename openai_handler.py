#!/usr/bin/env python3
import sys
import json
import os
from alfred_pyutils import Logger
from alfred_pyutils import Storage
from alfred_pyutils import StrUtils
from alfred_pyutils import OpenAiUtils
from openai_client import OpenAiClient

# File
# print(sys.argv[0])
# Query
# print(sys.argv[1])

_SUPPORTED_COMMANDS = ['openai_text_completion', 'openai_chat_completion', 'openai_image_generation']

# Empty input or whitespaces only
_input = sys.argv[1].strip()
if not _input:
    sys.exit(0)

# Split input into command and query
_input = _input.split(' ', 1)
if len(_input) != 2:
    sys.exit(0)

# Init
_logger = Logger(__name__)
_storage = Storage('storage.json')

# Create input object
_command = _input[0]
if _command not in _SUPPORTED_COMMANDS:
    sys.stdout.write(json.dumps({"items": [{"title": "Unrecognized command"}]}, ensure_ascii=False))
    sys.exit(0)

_query = _input[1]
_input_object = {"command": _command, "query": _query}
_input_json = json.dumps(_input_object, ensure_ascii=False)

# Check if there is a response for this query in the cache
if os.getenv("skip_cache") is None or os.getenv("skip_cache") == 'False':
    alfred_response = _storage.get_from_history_cache(_input_json)
    if alfred_response:
        _logger.debug(message='Returning response from cache..')
        sys.stdout.write(json.dumps(alfred_response, ensure_ascii=False))
        sys.exit(0)
else:
    _logger.debug(message='Skipping lookup in cache..')

# No response in cache, let's call OpenAI
_openai_client = OpenAiClient(auth_token=os.getenv("api_token"),
                              model_text_completion=os.getenv("model_text_completion"),
                              model_chat_completion=os.getenv("model_chat_completion"),
                              max_tokens=int(os.getenv("max_tokens")),
                              max_completions=int(os.getenv("max_completions")))

match _command:
    case 'openai_text_completion':
        openai_response = _openai_client.get_text_completion(_query)
        alfred_response = OpenAiUtils.create_alfred_response_from_openai_text_completion_response(openai_response)
    case 'openai_chat_completion':
        openai_response = _openai_client.get_chat_completion(_query)
        alfred_response = OpenAiUtils.create_alfred_response_from_openai_chat_completion_response(openai_response)
    case 'openai_image_generation':
        openai_response = _openai_client.get_image_completion(_query)
        alfred_response = OpenAiUtils.create_alfred_response_from_openai_image_generation_response(openai_response)
    case _:
        sys.stdout.write(json.dumps({"items": [{"title": "Unrecognized command"}]}, ensure_ascii=False))
        sys.exit(0)

if alfred_response:
    # Return data to Alfred
    _storage.add_to_history_cache(_input_json, alfred_response)
    sys.stdout.write(json.dumps(alfred_response, ensure_ascii=False))
