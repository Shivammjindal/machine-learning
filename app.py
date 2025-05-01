from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    result = {
        "user" : True
    }
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    print(username, password)

    return jsonify({
        "username" : "hello.py"
    })

if __name__ == '__main__':
    app.run(debug=True)
