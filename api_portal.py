from flask import Flask
import werkzeug 
werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restplus import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage 
from mfg import mfg_bd
from integration import int_bd
from utility import utility

app = Flask(__name__)
api = Api(app)

app.register_blueprint(mfg_bd, url_prefix='/ds/api/mfg')
app.register_blueprint(int_bd, url_prefix='/ds/api/int')
app.register_blueprint(int_bd, url_prefix='/ds/api/eng')
app.register_blueprint(utility, url_prefix='/ds/api')




if __name__ == '__main__':
  app.run(debug=True)