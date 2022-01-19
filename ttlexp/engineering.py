from flask import Blueprint
from flask_restx import Api

eng_bd = Blueprint('eng_api', __name__)
eng_api = Api(eng_bd)

@eng_bd.route('/hello/')
def hello():
  return "Hello from ENG Page"