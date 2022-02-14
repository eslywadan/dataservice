from flask import Flask
import werkzeug 
import tools.request_handler as req
from ttlexp.mfg import mfg_bd as mfg_api
from ttlexp.integration import int_bd as int_api
from ttlexp.engineering import eng_bd as eng_api
from tools.utility import utility as utility_api

app = Flask(__name__)

app.register_blueprint(utility_api, url_prefix='/ds/utility')
app.register_blueprint(mfg_api, url_prefix='/ds/mfg')
app.register_blueprint(int_api, url_prefix='/ds/int')
app.register_blueprint(eng_api, url_prefix='/ds/eng')


@app.route('/home/')
def home():
    return "Welcom Home!"


@app.route('/api/Login')
def login():
    #return "Welcome log in!"
    return req.process_login()


if __name__ == '__main__':
    app.run(debug=True,port=5000)