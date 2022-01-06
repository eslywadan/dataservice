from flask import Blueprint

mfg_bd = Blueprint('mfg', __name__)

@mfg_bd.route('/hello/')
def hello():
  return "Hello from MFG Page"
