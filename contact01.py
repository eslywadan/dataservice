from flask import Blueprint

contact_bd = Blueprint('contact01', __name__)

@contact_bd.route('/hello/')
def hello():
  return "Hello from Contact Page"