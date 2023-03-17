from model.model import spc_data_info
import json

class SpcYxInfo():
  """ info dict
	info = {"fab":fab,"chart_list":chart_list,"token":token,"start_dttm":start_dttm,"end_dttm":end_dttm,"method":method,
	"product":product, "pproc_id":pproc_id,"peqpt_id":peqpt_id,"precipe_id":precipe_id,"owner_code":owner_code,
	"run_mode":run_mode,"spc_item_id":spc_item_id,"proc_id":proc_id}"""
  def __init__(self,casefile,casename):
      self.load_cases(casefile, casename)

  def load_cases(self, casefile, casename):
      with open(casefile) as json_file:
        spcyx = json.load(json_file)
      
      case = spcyx[casename]
      self._info = spc_data_info(
        fab = case['fab'],
        chart_list = case['chart_list'],
        token = case['token'],
        start_dttm = case['start_dttm'],
        end_dttm = case['end_dttm'],
        method = case['method'],
        product = case['product'],
        pproc_id = case['pproc_id'],
        peqpt_id = case['peqpt_id'],
        precipe_id = case['precipe_id'],
        owner_code = case['owner_code'],
        run_mode = case['run_mode'],
        spc_item_id = case['spc_item_id'],
        proc_id = case['proc_id'])


  
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

from datetime import datetime

def casttime1(inputtime:str):
  datetime_object = datetime.strptime(inputtime, '%Y-%m-%d %H:%M:%S')
  return datetime_object.strftime("%Y%m%d%H%M%S") 