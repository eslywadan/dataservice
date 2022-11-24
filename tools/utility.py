from flask import Blueprint, send_file
from flask_restx import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
import tools.request_handler as req
from tools.response_handler import *
from pathlib import Path
from tools.request_handler import check_and_log as verified_token
from tools.celery_oper import *
from tools.general_fun import series2dic
import json

utility = Blueprint('utility_api', __name__)
utility_api = Api(utility)

@utility_api.route('/apikey/')
class GetApiKey(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('clientId', help='Specify your client id', location='args')
    parser.add_argument('password', help='Specify your client pass', location='args')
    @utility_api.doc(parser=parser)
    def get(self):
         # args = self.parser.parse_args()
         # client = args['clientId']
         # passward = args['password']
         # apikey = req.process_login(clientId=client,password=passward)
         apikey = req.process_login()
         return apikey

@utility_api.route('/orderstate/')
class OrderState(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('receipts', help='collect the receipts, seperate by "," for multiple ids', location='args')
    parser.add_argument('token', help='Specify your token id', location='args')
    @utility_api.doc(parser=parser)
    def get(self):
        receipts = series2dic(request.args.get('receipts'))
        res = chk_async_tasks(receipts)
        return JSNResponse(res)


@utility_api.route('/ordercontent/')
class OrderContent(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('receipt', help='the receipt id', location='args')
    parser.add_argument('token', help='Specify your token id', location='args')
    @utility_api.doc(parser=parser)
    def get(self):
        receipt = request.args.get('receipt')
        res = get_async_result(receipt)
        return JSNResponse(res)

        
@utility_api.route('/upload/')
class UploadDemo(Resource):
    upload_parser = utility_api.parser()
    upload_parser.add_argument('file',location='files',type=FileStorage)

    @utility_api.expect(upload_parser)
    def post(self):
        args = self.upload_parser.parse_args()
        file = args.get('file')
        print(file.filename)
        return "Upload file is " + file.filename

