#!/usr/bin/env python3
import sys
import json
from alfred_pyutils import Logger

_query = sys.argv[1].strip()

if not _query:
    sys.exit(0)

result = {
    "items": [
        {
            "type": "default",
            "title": "Press enter to send query",
            "subtitle": f"{_query}",
            "arg": f"{_query}",
            "autocomplete": "",
            "valid": True
        }
    ]
}

sys.stdout.write(json.dumps(result, ensure_ascii=False))
