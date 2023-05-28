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
from flask import abort, jsonify, request
from faces import create_app
from flask_restful import Api
from faces.resources.enroll import Enroll
from faces.resources.match import Match
from faces.detect import Detect


app = create_app()
api = Api(app)

@app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED.value)
def method_not_allowed(error):
    """Method not allowed 405 Response"""
    return jsonify(error=str(error)), HTTPStatus.METHOD_NOT_ALLOWED.value

@app.errorhandler(HTTPStatus.CONFLICT.value)
def conflict(error):
    """Conflict 409 Reponse."""
    return jsonify(error=str(error)), HTTPStatus.CONFLICT.value


api.add_resource(Enroll, '/register')
api.add_resource(Match, '/match')

if __name__ == '__main__':
    app.run()
