from flask import Blueprint

int_bd = Blueprint('integration', __name__)

@int_bd.route('/hello/')
def hello():
  return "Hello from INT Page"