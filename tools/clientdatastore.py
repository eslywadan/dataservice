import re
from tools.logger import Logger
from tools.innodrive import InnoDrive

class ClientDataStore():
  """"
  The class inherited InnoDrive with extented methods designed for 
  the client data store
  method get_client_folder : given the client id, will return the folder id created for the client
  method put_file : given enough the source file and target file paths... 
  """
  def __init__(self,**kwargs):
    """
      clientid -> the client id 
      sourcefilepath -> where path&file
      targetsubpath -> named data entity in full uri path 
    """
    self.parentnodeid = InnoDrive._nodeid
    try:
      clientid = kwargs['clientid']
    except:
      return None
    self.clientid = clientid
    self.clientds = InnoDrive(clientid=self.clientid)
    self.get_client_folder()

  def get_client_folder(self):
    self._folder_id = self.clientds.cds['id']
    
  def put_file(self,**kwargs):
    """"
    sfilepath = 'full path and the file name specify where the source'
    sfilename = 'source file name'
    tsubpath = 'target sub path where is under the client folder and before the file'
    tfilename = 'target file name'
    """
    try:
      sfilepath = kwargs['sfilepath']
      sfilename = kwargs['sfilename']
      tsubpath = kwargs['tsubpath']
      tfilename = kwargs['tfilename']
    except:
      return {}

    r1 = self.clientds.path_maker(self._folder_id,tsubpath,resetinfo=True)
    if r1["status"] == "OK": 
      endpointid = r1["endpoint"]
      resp1 = self.clientds.upload_file(sfilename, sfilepath, endpointid, tfilename)
      msg = f"file is saved as {self.clientid}{endpointid}"
      return { "status":200, "message":msg }
    else: return r1


  