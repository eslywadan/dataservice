from operator import index
from flask import Flask
from ttlexp.mfg import mfg_bd as mfg_api
from ttlexp.integration import int_bd as int_api
from ttlexp.engineering import eng_bd as eng_api
from tools.utility import utility as utility_api
import tools.request_handler as req

def create_app(config_filename=None):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_pyfile(config_filename)
  register_blueprint(app)
  return app

def register_blueprint(app):
  app.register_blueprint(utility_api, url_prefix='/ds/utility')
  app.register_blueprint(mfg_api, url_prefix='/ds/mfg')
  app.register_blueprint(int_api, url_prefix='/ds/int')
  app.register_blueprint(eng_api, url_prefix='/ds/eng')
  app.add_url_rule("/", view_func=index)
  app.add_url_rule("/home", view_func=home)
  app.add_url_rule("/api/Login", view_func=login)


def index():
    return "Index Page!"

def home():
    return "Welcom Home!"

def login():
    return req.process_login()