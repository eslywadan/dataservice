from flask import Flask
import werkzeug 
import tools.request_handler as req
from ttlexp import create_app


app=create_app('flask.cfg')

@app.route('/home/')
def home():
    return "Welcom Home!"


@app.route('/api/Login')
def login():
    #return "Welcome log in!"
    return req.process_login()


if __name__ == '__main__':
    app.run(debug=True,port=5000)