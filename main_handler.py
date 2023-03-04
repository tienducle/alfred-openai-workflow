#!/usr/bin/env python3
import sys
import json
from alfred_pyutils import Logger

_LOGGER = Logger(__name__)

_query = sys.argv[1].strip()

if not _query:
    sys.exit(0)

_LOGGER.debug(sys.version)

result = {
    "items": [
        {
            "uid": "text_completion",
            "type": "default",
            "title": "OpenAI Text Completion",  # main text in result entry
            "subtitle": f"Send '{_query}' to OpenAI Text Completion API",
            # "arg": '{"command": "openai_chat_completion", "query": "' + f"{_query}" + '"}',  # this text will be forwarded to next node in workflow
            "arg": f"openai_text_completion {_query}",
            "autocomplete": "",  # f"gpt-text-completion {_query}",  # this text will be inserted into input field when the user presses tab
            "valid": True  # if True, this item can be selected and arg will be forwarded to next node
            # if False, autocomplete will be inserted into input field on pressing Enter
        },
        {
            "uid": "chat_completion",
            "type": "default",
            "title": "OpenAI Chat Completion",  # main text in result entry
            "subtitle": f"Send '{_query}' to OpenAI Chat Completion API",
            # "arg": '{"command": "openai_chat_completion", "query": "' + f"{_query}" + '"}',  # this text will be forwarded to next node in workflow
            "arg": f"openai_chat_completion {_query}",
            "autocomplete": "",  # f"gpt-chat-completion {_query}",  # this text will be inserted into input field when the user presses tab
            "valid": True  # if True, this item can be selected and arg will be forwarded to next node
            # if False, autocomplete will be inserted into input field on pressing Enter
        },
        {
            "uid": "image_generation",
            "type": "default",
            "title": "OpenAI Image Generation",  # main text in result entry
            "subtitle": f"Send '{_query}' to OpenAI Image Generation API",
            # "arg": '{"command": "openai_chat_completion", "query": "' + f"{_query}" + '"}',  # this text will be forwarded to next node in workflow
            "arg": f"openai_image_generation {_query}",
            "autocomplete": "",  # f"gpt-chat-completion {_query}",  # this text will be inserted into input field when the user presses tab
            "valid": True  # if True, this item can be selected and arg will be forwarded to next node
            # if False, autocomplete will be inserted into input field on pressing Enter
        }
    ]
}

sys.stdout.write(json.dumps(result, ensure_ascii=False))
