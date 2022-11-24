# from flask import Flask
# import werkzeug 
# import tools.request_handler as req
from ttlexp import create_app
from flask_cors import CORS

app=create_app('flask.cfg')
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)