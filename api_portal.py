from flask import Flask
import werkzeug 
werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from testapi import pizza_bd as pizza_api
from utility import utility as utility_api
from mfg import mfg_bd as mfg_api
from integration import int_bd as int_api
from engineering import eng_bd as eng_api

app = Flask(__name__)

app.register_blueprint(pizza_api, url_prefix='/ds/test')
app.register_blueprint(utility_api, url_prefix='/ds/utility')
app.register_blueprint(mfg_api, url_prefix='/ds/mfg')
app.register_blueprint(int_api, url_prefix='/ds/int')
app.register_blueprint(eng_api, url_prefix='/ds/eng')


@app.route('/home/')
def home():
  return "Welcom Home!"


if __name__ == '__main__':
  app.run(debug=True)