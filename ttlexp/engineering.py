from datetime import date
import string
from flask import Blueprint,request
from flask_restx import Api, Resource, fields, reqparse
import json
from tools.error_handler import JSNError
import tools.request_handler as req 
from ttlsap.sa_eng import EdcRawApi 

eng_bd = Blueprint('eng_api', __name__)
eng_api = Api(eng_bd)

edcrawapi = EdcRawApi()

@eng_bd.route('/hello/')
def hello():
	return "Hello from ENG Page"

#edcraw_model = eng_api.model('Edcraw',{
#    'GLASS_ID': fields.String(attribute='GLASS_ID'),
#    'TRANSDT': fields.String(attribute='TRANSDT'),
#    'PRODUCT_ID': fields.String(attribute='PRODUCT_ID'),
#    'CHAMBER': fields.String(attribute='CHAMBER'),
#    'OPER': fields.String(attribute='OPER'),
#    'RECIPE_ID': fields.String(attribute='RECIPE_ID'),
#    'OWNER': fields.String(attribute='OWNER')
#    'ITEM': fields.String(attribute='ITEM'),
#    'Value': fields.String(attribute='VALUE')
#})

edc_parser = eng_api.parser()
edc_parser.add_argument('start_time', type=str,  help='Required start time by date,ex:20220114140000')
edc_parser.add_argument('end_time', type=str, help='Required start time by date,ex:20220114160000')
edc_parser.add_argument('sub_equip', type=str, help='Optional if sub_equip is diff with equip,ex:PFRW0100')
# edc_parser.add_argument('grp_id', type=str, help='Optional, data provided only for specified glass id')
edc_parser.add_argument('token', type=str, help='Optional token')
@eng_api.route('/edcraw/<string:fab>/<string:equip>/items/<string:items>', methods=['GET'])
class EdcRaw(Resource):

    @eng_api.doc('EDC Raw NDE')
    @eng_api.expect(edc_parser)
    # @eng_api.marshal_with(edcraw_model)
    def get(sellf, fab, equip, items):
        chk_perm = req.check_and_log(ignore_token=False)
        if chk_perm is not True:  return chk_perm

        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        sub_equip = request.args.get('sub_equip')

        data = []
        for item in items.split(","):
            data.append(edcrawapi.edcrawbytime(fab=fab,equip=equip,edc=item,start_time=start_time,
            end_time=end_time,sub_eq=sub_equip,grp_id=''))

        return req.JSNResponse(data)




