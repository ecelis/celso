from flask import redirect, request, g
from faces import create_app
from faces import video_transform_track
from faces import detect

app = create_app()

@app.route('/register', methods=['POST'])
def register():
    error = None
    id_encodings = None
    if request.method == 'POST':
        json = request.get_json()
        id = json['id']
        id_encodings = detect.encode(id)
        return {'id': id}
    else:
        error = 'Bad request'
    return {error: error}

if __name__ == '__main__':
    app.run()

