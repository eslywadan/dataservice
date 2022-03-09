from flask import Blueprint, request
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

@mfg_api.route('/qtime/<string:fab>/products/<string:list_prods>', methods=['GET'],endpoint='qtime')
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


    @mfg_api.doc('qtime NDE')
    @mfg_api.marshal_with(qtime_model, envelope='qtime')
    def get(self, fab, prod=None, list_prods=None):
        #if not req.check_and_log(ignore_token=False):
        #    return JSNError("Tokenn is missing or token is not correct, #please login api to get a new token.",status_code=404)
        
        if list_prods is not None:
            prod_list = list_prods.split(",")
        if prod is not None:
            prod_list = prod

        data = []
        for prod in prod_list:
            data.append(sa_mfg.productqtime(fab,prod))

        return data

