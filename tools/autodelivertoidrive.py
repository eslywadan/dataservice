from tools.innodrive import InnoDrive

class InnoDriveForClient(InnoDrive):
  """Treat a part of the InnoDrive as owned by the client when hadeling the data file """



  def get_anchor(self, clientnodeid, ):
    self.clientnode 