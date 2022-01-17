from flask import Blueprint
from flask_restplus import Api, Resource, fields, reqparse
import json
from apis.sa_mfg import MfgApi 

mfg_bd = Blueprint('mfg_api', __name__)
mfg_api = Api(mfg_bd)
sa_mfg = MfgApi()


@mfg_bd.route('/hello/')
def hello():
  return "Hello from MFG Page"

@mfg_api.route('/qtime/<string:fab>/<string:prod>')
@mfg_api.route('/<string:prod>/<string:fab>/qtime')
class ProdQtime(Resource):
    qtime_model = mfg_api.model('Qtime', {
      'PRODUCT_ID': fields.String(attribute='PRODUCT_ID'),
      'ROUTE_ID': fields.String(attribute='ROUTE_ID'),
      'OPE_ID': fields.String(attribute='OPE_ID'),
      'QRS_ID': fields.String(attribute='QRS_ID'),
      'QRS_OPE_ID': fields.String(attribute='QRS_OPE_ID'),
      'QRS_TIME': fields.String(attribute='QRS_TIME'),
      'QRK_TIME': fields.String(attribute='QRK_TIME')
    })

    @mfg_api.doc()
    @mfg_api.marshal_with(qtime_model, envelope='qtime')
    def get(self, fab, prod):
        data = sa_mfg.productqtime(fab,prod)
        return data

    @mfg_api.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        mfg_api.abort(403)
