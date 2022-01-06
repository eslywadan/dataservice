from flask import Flask
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
import werkzeug 
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage 
# from home import home_bp
# from contact import contact_bp

"""https://towardsdatascience.com/creating-restful-apis-using-flask-and-python-655bad51b24"""

"""https://medium.com/analytics-vidhya/swagger-ui-dashboard-with-flask-restplus-api-7461b3a9a2c8"""



app = Flask(__name__)
api = Api(app)

# app.register_blueprint(home_bp, url_prefix='/home')
# app.register_blueprint(contact_bp, url_prefix='/contact')


upload_parser = api.parser()
upload_parser.add_argument('file',
                           location='files',
                           type=FileStorage)

@api.route('/upload/')
@api.expect(upload_parser)
class UploadDemo(Resource):
  def post(self):
    args = upload_parser.parse_args()
    file = args.get('file')
    print(file.filename)
    return "Upload file is " + file.filename


if __name__ == '__main__':
  app.run(debug=True)