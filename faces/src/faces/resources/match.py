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
from marshmallow import ValidationError
from faces.detect import Detect


class Match(Resource):
    """Match faces against enrolled ones"""

    def post(self):
        """Identify faces and return match success or denied."""
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('picture', required=True, type=str,
                                 action='append', help='User face picture list')
        args = post_parser.parse_args()
        print(args)
        try:
            # data = user_schema.load(args)  TODO can Schema be used in Login POST?
            detect = Detect(None)
            result = detect.match(args['picture'][0])
            error = result.get('error', None)
            if not error:
                return result, HTTPStatus.ACCEPTED
            error = 'Unable to register face, either it is already registered, non-human or database issue.'  # pylint: disable=line-too-long
            abort(HTTPStatus.CONFLICT.value,
                description=error)
        except ValidationError as error:
            return error.messages, HTTPStatus.INTERNAL_SERVER_ERROR
