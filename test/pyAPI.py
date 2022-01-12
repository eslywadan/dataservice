from flask import Flask, jsonify, Response
import json

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/test_api/', methods=['GET'])
def test_api():
  return jsonify(message='Hello, API')

@app.route('/test_api2', methods=['GET'])
def test_api2():
  return json.dumps('Hello, API2')

@app.route('/test_api3', methods=['GET'])
def test_api3():
  return Response(json.dumps({'messasge':'Hello, API2'}), mimetype='application/json')


if __name__ == '__main__':
  app.run(debug=True)