from flask import Blueprint
from flask_restx import Api, Resource, fields, reqparse
import json
from tools.response_handler import JSNResponse, JSNError
import tools.request_handler as req

int_bd = Blueprint('int_api', __name__)
int_api = Api(int_bd)

@int_bd.route('/hello/')
def hello():
  return "Hello from INT Page"