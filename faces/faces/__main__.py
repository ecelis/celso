from bson import ObjectId
import json
from flask import redirect, request, g
from faces import create_app
from faces import video_transform_track
from faces.detect import Detect
from faces.util import MongoJSONEncoder

app = create_app()

@app.route('/register', methods=['POST'])
def register():
    error = None
    if request.method == 'POST':
        json = request.get_json()
        id = json['id']
        detect = Detect()
        result = detect.encode(id)
        if (result.acknowledged):
            json_data = MongoJSONEncoder().encode(result.inserted_id)
            return {'id': json_data.replace('"', '')}
        else:
            error = 'Unable to register face'
    else:
        error = 'Bad request'
    return {'error': error}

if __name__ == '__main__':
    app.run()

