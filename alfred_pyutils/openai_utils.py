#!/usr/bin/env python3
from alfred_pyutils import Logger

_LOGGER = Logger(__name__)


class OpenAiUtils:

    @staticmethod
    def __get_clean_text(text):
        completed_pre_processing = False
        while not completed_pre_processing:
            old_length = len(text)
            text = text.strip('?').strip(',').strip()
            if len(text) == old_length:
                completed_pre_processing = True
        return text

    @staticmethod
    def transform_text_completion_choices(openai_response_data):
        items = []
        for item in openai_response_data['choices']:
            items.append(item['text'])
        return items

    @staticmethod
    def transform_chat_completion_choices(openai_response_data):
        items = []
        for item in openai_response_data['choices']:
            items.append(item['message']['content'])
        return items

    @staticmethod
    def transform_image_generation_urls(openai_response_data):
        items = []
        for item in openai_response_data['data']:
            items.append(item['url'])
        return items

    @staticmethod
    def create_alfred_response_from_openai_text_completion_response(openai_response_data):
        return OpenAiUtils.__create_alfred_response_from_openai_response(openai_response_data,
                                                                         OpenAiUtils.transform_text_completion_choices)

    @staticmethod
    def create_alfred_response_from_openai_chat_completion_response(openai_response_data):
        return OpenAiUtils.__create_alfred_response_from_openai_response(openai_response_data,
                                                                         OpenAiUtils.transform_chat_completion_choices)

    @staticmethod
    def create_alfred_response_from_openai_image_generation_response(openai_response_data):
        return OpenAiUtils.__create_alfred_response_from_openai_response(openai_response_data,
                                                                         OpenAiUtils.transform_image_generation_urls)

    @staticmethod
    def __create_alfred_response_from_openai_response(openai_response_data, items_handler):
        response_id = openai_response_data['id'] if 'id' in openai_response_data else 'no_id'
        # response_object = openai_response_data['object']
        # created = openai_response_data['created']
        # model = openai_response_data['model']
        # usage_object = openai_response_data['usage']

        result = {"items": []}
        index = 0
        for item in items_handler(openai_response_data):
            text = OpenAiUtils.__get_clean_text(item)
            result["items"].append(
                {
                    "uid": response_id + "-" + str(index),
                    "type": "default",
                    #"title": "Response " + str(index),  # main text in result entry
                    "title": text,  # main text in result entry
                    "subtitle": text,
                    "arg": text,  # this text will be forwarded to next node in workflow
                    "autocomplete": text,  # this text will be inserted into input field when the user presses tab
                    "valid": True  # if True, this item can be selected and arg will be forwarded to next node
                    # if False, autocomplete will be inserted into input field on pressing Enter
                }
            )
            index += 1
        return result


