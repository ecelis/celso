from flask import redirect, request
from faces import create_app


app = create_app()

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']

if __name__ == '__main__':
    app.run(debug=True)

