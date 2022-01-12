from flask import Blueprint
from flask_restplus import Api, Resource

mfg_bd = Blueprint('mfg_api', __name__)
mfg_api = Api(mfg_bd)

@mfg_bd.route('/hello/')
def hello():
  return "Hello from MFG Page"

@mfg_api.doc(params={'id': 'An ID'})
class MyResource(Resource):
    def get(self, id):
        return "Hello from MFG Page"

    @mfg_api.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        mfg_api.abort(403)
