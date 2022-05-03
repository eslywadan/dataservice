from flask import Flask
import werkzeug 
import tools.request_handler as req
from ttlexp import create_app


app=create_app('flask.cfg')


if __name__ == '__main__':
    app.run(debug=True,port=5000)