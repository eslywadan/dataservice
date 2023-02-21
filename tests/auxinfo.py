from model.model import spc_data_info


class SpcYxInfo():
  """ info dict
	info = {"fab":fab,"chart_list":chart_list,"token":token,"start_dttm":start_dttm,"end_dttm":end_dttm,"method":method,
	"product":product, "pproc_id":pproc_id,"peqpt_id":peqpt_id,"precipe_id":precipe_id,"owner_code":owner_code,
	"run_mode":run_mode,"spc_item_id":spc_item_id,"proc_id":proc_id}"""
  def __init__(self):
      self.fab = "T7"
      self.chart_list = ""
      self.token = ""
      self.start_dttm = "2022-08-02 08:00:00"
      self.end_dttm = "2022-12-22 17:00:00"
      self.method = ""
      self.product = "TJDF40XK"
      self.pproc_id="4300"
      self.peqpt_id="TLCD0300"
      self.precipe_id = "DF40XK_A5_4_254A"
      self.owner_code = "CRN0"
      self.run_mode = "N"
      self.spc_item_id = "MB_X"
      self.proc_id = "438N"
      self.info()
      
  def info(self):
    self._info = spc_data_info(fab=self.fab,chart_list=self.chart_list,token=self.token,start_dttm=self.start_dttm,end_dttm=self.end_dttm,method=self.method,
	product=self.product, pproc_id=self.pproc_id,peqpt_id=self.peqpt_id,precipe_id=self.precipe_id,owner_code=self.owner_code,
	run_mode=self.run_mode,spc_item_id=self.spc_item_id,proc_id=self.proc_id)


  
class TrailArg():
    """"registed tsid
      'edcrawasync1' : arguments set for trail of accessing asynchronous edcraw data service 
      'spcyxasync1' : arguments set for trial of accessing asynchronous spcyx data service
    """
    args = {}

    def __init__(self,tsid):
        if tsid == 'edcrawasync1': self.edcrawasync1()
        if tsid == 'spcyxasync1': self.spcyxasync1()

    def edcrawasync1(self):
        self.args = {}
        self.args['req_count'] = 1
        self.args['fab'] = 'TFTT6'
        self.args['equip'] = 'CVDA0100'
        self.args['item'] = '1GAS1'
        self.args['start_time'] = '20220401000000'
        self.args['end_time'] = '20220402160000'
        self.args['sub_equip'] = 'CVDA0100'
        self.args['saved_filenanme'] = 'test_edcrawasync.csv'
        self.args['clientid'] = 'test_client'

    def spcyxasync1(self):
        self.args['fab'] = "TFT7"
        self.args['chart_list'] = ""
        self.args['token'] = ""
        self.args['start_dttm'] = "20220712080000"
        self.args['end_dttm'] = "20220712170000"
        self.args['method'] = ""
        self.args['product'] = "TJDF40XK"
        self.args['pproc_id']="4300"
        self.args['peqpt_id']="TLCD0300"
        self.args['precipe_id'] = "DF40XK_A5_4_254A"
        self.args['owner_code'] = "CRN0"
        self.args['run_mode'] = "N"
        self.args['spc_item_id'] = "MB_X"
        self.args['proc_id'] = "438N"
        self.args['clientid'] = 'eng'
        self.args['nd'] = 'spcyx'