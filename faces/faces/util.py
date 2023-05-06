import os
import json
from datetime import datetime
from typing import Any

from bson import ObjectId


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

def make_dir(dir_fd):
    os.mkdir(dir_fd, 0o700)
