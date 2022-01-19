from flask import Blueprint
from flask_restx import Api

int_bd = Blueprint('int_api', __name__)
int_api = Api(int_bd)

@int_bd.route('/hello/')
def hello():
  return "Hello from INT Page"