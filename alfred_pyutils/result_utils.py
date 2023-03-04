#!/usr/bin/env python3
from alfred_pyutils import Logger

_LOGGER = Logger(__name__)


class ResultUtils:

    @staticmethod
    def create_result_item(uid: str,
                           item_type: str,
                           title: str,
                           subtitle: str,
                           arg: str,
                           icon: object,
                           autocomplete: str,
                           valid: bool) -> object:
        """
        Creates a result item for Alfred
        :param str uid: (optional) A unique identifier for the item. It allows Alfred to learn about the item for
        subsequent sorting and ordering of the user's actioned results.
        :param str item_type: By specifying "type": "file", Alfred treats your result as a file on your system.
        This allows the user to perform actions on the file like they can with Alfred's standard file filters.
        :param str title: (optional) The subtitle displayed in the result row.
        :param str subtitle: (optional) The subtitle displayed in the result row.
        :param str|array arg: The argument which is passed through to the next node in the workflow.
        :param object icon: The icon displayed in the result row. You can use relative paths to reference icons stored
        in your workflow's folder: "icon": {"path": "./custom_icon.png"}
        :param str autocomplete: This text will be inserted into input field when the user presses tab
        :param bool valid: (optional) If True, this item can be selected and arg will be forwarded to next node.
        If False, autocomplete will be inserted into input field on pressing Enter.
        :return: object
        """

        result = {'title': title, 'arg': arg}
        if uid:
            result['uid'] = uid
        if item_type:
            result['type'] = item_type
        if subtitle:
            result['subtitle'] = subtitle
        if icon:
            result['icon'] = icon
        if autocomplete:
            result['autocomplete'] = autocomplete
        if valid:
            result['valid'] = valid

        return result
