from flask import Blueprint

home_bd = Blueprint('home', __name__)

@home_bd.route('/hello/')
def hello():
  return "Hello from Home Page"