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

from flask import request
from faces import create_app
from faces.detect import Detect
from faces.util import MongoJSONEncoder

app = create_app()

@app.route('/register', methods=['POST'])
def register():
    """Register new face encodings endpoint."""
    error = None
    if request.method == 'POST':
        json_data = request.get_json()
        _id = json_data['id']
        username = json_data['username']
        detect = Detect()
        result = detect.encode(_id, username)
        if result.acknowledged:
            _id = MongoJSONEncoder().encode(result.inserted_id)
            return {'id': _id.replace('"', '')}
        error = 'Unable to register face'
    else:
        error = 'Bad request'
    return {'error': error}

@app.route('/match', methods=['POST'])
def match():
    """Match a face against known sample encodings."""
    error = None
    if request.method == 'POST':
        json_data = request.get_json()
        detect = Detect()
        result = detect.match(json_data['picture'])
        error = result.get('error', None)
        if not error:
            return result
        error = result['error']
    return {'error': error}

if __name__ == '__main__':
    app.run()
