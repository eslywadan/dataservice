from flask import request, Response, json
from grpc_cust.clientapival_client import get_verified_apikey

from tools.logger import Logger

#繼承Response，預設status code:200，預設mimetype:application/json
class JSNResponse(Response):
    def __init__(self, payload, status_code=200):
        Response.__init__(self, json.dumps(payload))
        self.status_code = status_code
        self.mimetype = 'application/json'
        req_info = request_info()
        Logger.log(f'{req_info}')
        Logger.log(f'End request: {status_code}')
        

class InvalidUsage(Response):
    def __init__(self, message, status_code=400, payload=None):
        Response.__init__(self, json.dumps(payload))
        self.status_code = status_code
        self.mimetype = 'application/json'
        req_info = request_info()
        Logger.log(f'{req_info}')
        Logger.log(f'End request: {status_code}')


class JSNError(Response):
    def __init__(self, payload, status_code=500):
        Response.__init__(self, json.dumps(payload))
        self.status_code = status_code
        self.mimetype = 'application/json'
        req_info = request_info()
        Logger.log(f'{req_info}')
        Logger.log(f'End request: {status_code}')


def request_info():

    req_url = request.url
    client_id = ""
    given_token = None
    if "clientId" in request.headers:
        client_id = request.headers["clientId"]
    else:
        client_id = request.args.get('client')

    if "apikey" in request.headers: 
        given_token = request.headers["apikey"]

    if request.args.get('token'):
        given_token = request.args.get('token')

    if given_token is not None:
        token_info =  get_verified_apikey(given_token)
        client_id = token_info.assertion.split(":")[0]

    info = "Requested URL: %s, client_id :%s, given_token:%s" %(req_url,client_id, given_token ) 
    return info

        