from flask import Blueprint, request
from flask_restx import Api, Resource, fields, reqparse
import json
from tools.response_handler import *
from tools.request_handler import check_and_log as verified_token
from ttlsap.sa_mfg import MfgApi 

mfg_bd = Blueprint('mfg_api', __name__)
mfg_api = Api(mfg_bd)
sa_mfg = MfgApi()


@mfg_bd.route('/hello/')
def hello():
    return "Hello from MFG Page"


#qtime_model = mfg_api.model('Qtime', {
#    'PRODUCT_ID': fields.String(attribute='PRODUCT_ID'),
#    'ROUTE_ID': fields.String(attribute='ROUTE_ID'),
#    'OPE_ID': fields.String(attribute='OPE_ID'),
#    'QRS_ID': fields.String(attribute='QRS_ID'),
#    'QRS_OPE_ID': fields.String(attribute='QRS_OPE_ID'),
#    'QRS_TIME': fields.String(attribute='QRS_TIME'),
#    'QRK_TIME': fields.String(attribute='QRK_TIME')
#})

mfg_parser = mfg_api.parser()
mfg_parser.add_argument('token', type=str, help='Optional token')
@mfg_api.route('/qtime/<string:fab>/products/<string:list_prods>', methods=['GET'],endpoint='prdqtime')
class ProdQtime(Resource):

    @mfg_api.doc('qtime NDE')
    @mfg_api.expect(mfg_parser)
    # @mfg_api.marshal_with(qtime_model, mask='token')
    def get(self, fab, prod=None, list_prods=None):
        chk_perm = verified_token(ignore_token=False)
        if chk_perm["status"] is not True:  return chk_perm["error_msg"]

        if list_prods is not None:
            prod_list = list_prods.split(",")
        if prod is not None:
            prod_list = prod

        data = []
        for prod in prod_list:
            data.append(sa_mfg.productqtime(fab,prod))

        return JSNResponse(data)


@mfg_api.route('/recipe/<string:fab>/products/<string:list_prods>', methods=['GET'],endpoint='prdrecipe')
class PrdRecipe(Resource):

    @mfg_api.doc('Products Recipe NDE')
    @mfg_api.expect(mfg_parser)
    # @mfg_api.marshal_with(recipe_model, mask='token')
    def get(self, fab, prod=None, list_prods=None):
        chk_perm = verified_token(ignore_token=False)
        if chk_perm["status"] is not True:  return chk_perm["error_msg"]

        if list_prods is not None:
            prod_list = list_prods.split(",")
        if prod is not None:
            prod_list = prod

        data = []
        for prod in prod_list:
            data.append(sa_mfg.productrecipe(fab,prod))

        return JSNResponse(data)

    
@mfg_api.route('/route/<string:fab>/products/<string:list_prods>', methods=['GET'],endpoint='prdroute')
class PrdRoute(Resource):

    @mfg_api.doc('Products Route NDE')
    @mfg_api.expect(mfg_parser)
    # @mfg_api.marshal_with(recipe_model, mask='token')
    def get(self, fab, prod=None, list_prods=None):
        chk_perm = verified_token(ignore_token=False)
        if chk_perm["status"] is not True:  return chk_perm["error_msg"]

        if list_prods is not None:
            prod_list = list_prods.split(",")
        if prod is not None:
            prod_list = prod

        data = []
        for prod in prod_list:
            data.append(sa_mfg.productroute(fab,prod))

        return JSNResponse(data)

