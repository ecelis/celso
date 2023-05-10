"""
Celso FaceID by @ecelis
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
