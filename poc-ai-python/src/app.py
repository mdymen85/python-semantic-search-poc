from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Hello, World!")

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    name = data.get('name')
    return jsonify(message=f"Received name: {name}")

if __name__ == '__main__':
    app.run(debug=True)