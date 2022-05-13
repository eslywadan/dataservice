import grpc
import grpc_cust.valclient_pb2 as valclient_pb2
import grpc_cust.valclient_pb2_grpc as valclient_pb2_grpc
from tools.config_loader import ConfigLoader

__all__ = {
  'client_info'
}

valclient_server = ConfigLoader.config("grpc")["valclient"]["server"]
valclient_port = ConfigLoader.config("grpc")["valclient"]["port"]

SERVER_ADDRESS = "%s:%s" %(valclient_server,valclient_port)


def simplemethod(stub,client):
  print("------------------Call Simple Method Begin-----------------")
  
  print("response from server(%s)" %SERVER_ADDRESS)
  request = valclient_pb2.Request(client_id=client)
  response = stub.ElaborDetail(request)
  print("response info(%s)" %response)
  print("-----------------Call simplemethod over ------------------")
  return response


def client_info(client):
  with grpc.insecure_channel(SERVER_ADDRESS) as channel:
    stub = valclient_pb2_grpc.ValclientStub(channel)

    return simplemethod(stub,client)
