# from flask import Flask
# import werkzeug 
# import tools.request_handler as req
from ttlexp import create_app


app=create_app('flask.cfg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8060)