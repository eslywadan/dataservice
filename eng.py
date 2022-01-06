from flask import Blueprint

eng_bd = Blueprint('engineering', __name__)

@eng_bd.route('/hello/')
def hello():
  return "Hello from ENG Page"