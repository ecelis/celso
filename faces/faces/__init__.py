import os
from flask import Flask
from flask_cors import CORS



db = []

sample_path = os.environ.get('CELSO_SAMPLES', '/tmp/samples')
unkown_path = os.environ.get('CELSO_UNKNOWN', '/tmp/unknown')

if not os.path.exists(sample_path):
   os.mkdir(sample_path, 0o700)
if not os.path.exists(unkown_path):
    os.mkdir(unkown_path, 0o700)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return {'Sobre el Rio, version': '0.0.1'}
    
    return app

