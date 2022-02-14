from flask import Blueprint
from flask_restx import Api, Resource, fields, reqparse
import json
from tools.error_handler import JSNError
import tools.request_handler as req 
from ttlsap.sa_mfg import MfgApi 

mfg_bd = Blueprint('mfg_api', __name__)
mfg_api = Api(mfg_bd)
sa_mfg = MfgApi()


@mfg_bd.route('/hello/')
def hello():
    return "Hello from MFG Page"


@mfg_api.route('/qtime/<string:fab>/<string:prod>')
@mfg_api.route('/<string:prod>/<string:fab>/qtime')
@mfg_api.route('/qtime/<fab>/products', methods=['POST'])
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
        if not req.check_and_log(ignore_token=False):
            return JSNError("Tokenn is missing or token is not correct, please login api to get a new token. ")

        data = sa_mfg.productqtime(fab,prod)
        return data

    @mfg_api.doc()
    @mfg_api.marshal_with(qtime_model, envelope='qtime')
    def post(self,  fab):
        if not req.check_and_log():
            return "Token is missing or token is not correct, please login api to get a new token. ", 401
      
        posted = json.loads(request.data.decode("utf-8"))
        if posted: 
            if "prod_list" in posted: prod_list = posted["prod_list"] 
            else: return
        else: return
    
        data = []
        for prod in prod_list:
            data.append(sa_mfg.productqtime(fab,prod))

        return data