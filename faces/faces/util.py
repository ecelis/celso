"""
Utility functions for Celso FaceID by @ecelis
"""

import json
from datetime import datetime
from typing import Any

from bson import ObjectId


class MongoJSONEncoder(json.JSONEncoder):
    """Add support for ObjetId to JSONEncoder"""
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)
