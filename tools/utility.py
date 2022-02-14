from flask import Blueprint
from flask_restx import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage

utility = Blueprint('utility_api', __name__)
utility_api = Api(utility)

@utility_api.route('/hello/')
class HelloWorld(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', help='Specify your name')
    @utility_api.doc(parser=parser)
    def get(self):
        args = self.parser.parse_args()
        name = args['name']
        return "Hello! " + name
  

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