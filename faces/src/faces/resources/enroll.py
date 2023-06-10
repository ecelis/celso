"""
Celso FaceID by @ecelis

   Copyright 2023 Ernesto A. Celis de la Fuente

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from http import HTTPStatus
from flask import abort
from flask_restful import reqparse, Resource
from marshmallow import ValidationError, Schema, fields
from faces.detect import Detect
from faces.common.helpers import get_db
from faces.common.util import MongoJSONEncoder


def must_not_be_blank(data):
    """Raise ValidationError when empty data"""
    if not data:
        raise ValidationError("Data not provided")

UserSchema = Schema.from_dict({
    "_id": fields.Str(dump_only=True),
    "username": fields.Str(),
    "picture": fields.List(cls_or_instance=fields.Str),

})

user_schema = UserSchema()

class Enroll(Resource):
    """Enroll faces for ID"""

    def post(self):
        """Register new face encodings endpoint."""
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('username', required=True, type=str,
                                 help='Username')
        post_parser.add_argument('picture', required=True, type=str,
                                 action='append', help='User face picture list')
        args = post_parser.parse_args()
        try:
            data = user_schema.load(args)
            detect = Detect(get_db())
            result = detect.encode(data['picture'], data['username'])
            if result['success']:
                encoded_data = result['data']
                if encoded_data.acknowledged:
                    _id = MongoJSONEncoder().encode(encoded_data.inserted_id)
                    return {
                        'id': _id.replace('"', ''),
                        'username': data['username']
                        }, HTTPStatus.CREATED
            error = 'Unable to register face, either it is already registered, non-human or database issue.'  # pylint: disable=line-too-long
            abort(HTTPStatus.CONFLICT.value,
                description=error)
        except ValidationError as error:
            return error.messages, HTTPStatus.UNPROCESSABLE_ENTITY
