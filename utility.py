from flask import Blueprint

utility = Blueprint('utility', __name__)

upload_parser = api.parser()
upload_parser.add_argument('file',
                           location='files',
                           type=FileStorage)

@utility.route('/upload/')
def upload_csv():
  return "Upload CSV function"