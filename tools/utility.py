from flask import Blueprint
from flask_restx import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
import tools.request_handler as req

utility = Blueprint('utility_api', __name__)
utility_api = Api(utility)

@utility_api.route('/apikey/')
class HelloWorld(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('client', help='Specify your client id')
    parser.add_argument('passward', help='Specify your client pass')
    @utility_api.doc(parser=parser)
    def get(self):
        args = self.parser.parse_args()
        client = args['client']
        passward = args['passward']
        apikey = req.process_login(clientId=client,password=passward)
        return apikey
  

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