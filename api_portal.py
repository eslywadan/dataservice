from flask import Flask
import werkzeug 
import tools.request_handler as req
<<<<<<< HEAD
from ttlexp.mfg import mfg_bd as mfg_api
from ttlexp.integration import int_bd as int_api
from ttlexp.engineering import eng_bd as eng_api
from tools.utility import utility as utility_api
from ttlsap.adapter.intrpt import IntRptConnect
=======
from ttlexp import create_app
>>>>>>> main


app=create_app('flask.cfg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8060)