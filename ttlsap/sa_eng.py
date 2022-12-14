import requests
import json
from tools.config_loader import ConfigLoader
from ttlsap.adapter.intrpt import IntRptConnect
from ttlsap.adapter.intrpt2 import IntRptConnect2

from tools.clientdatastore import ClientDataStore

class EdcRawApi():

    def __init__(self):
      pass

    def edcrawbytime(cls,**kwargs):
      selQryType = "T"
      intrpt = IntRptConnect()
      intrpt.get_apikey()
      edcmap = ConfigLoader.config("edcfabmap")
      fab = edcmap[kwargs['fab']]

      intrpt.filcrit_edcraw(fab=fab,selQryType=selQryType,FromDate=kwargs['start_time'],
        ToDate=kwargs['end_time'],txtIDList=kwargs['grp_id'],selMainEQP=kwargs['equip'],
        selSubEQP=kwargs['sub_eq'],selEDCItem=kwargs['edc'])

      funname = 'EDC_RAW_'+ fab.split("_")[0]
      intrpt.linkpage(funname)
      data = intrpt.request_api()
      cls.url = intrpt.url
      cls.linkpageencode = intrpt.linkpageencode
      cls.filter = intrpt.filter
      cls.filterencode = intrpt.filterencode
      cls.linkkey = intrpt.linkkey
      cls.apikey = intrpt.apikey
      return data

    def edcnetbytime(cls,**kwargs):
      """"Use the new implementaion of source adapter IntRptConnect2 which will connect to newer source api server"""
      selQryType = "T"
      intrpt = IntRptConnect2()
      edcmap = ConfigLoader.config("edcfabmap")
      fab = edcmap[kwargs['fab']]

      intrpt.filcrit_edcraw(fab=fab,selQryType=selQryType,FromDate=kwargs['start_time'],
        ToDate=kwargs['end_time'],txtIDList=kwargs['grp_id'],selMainEQP=kwargs['equip'],
        selSubEQP=kwargs['sub_eq'],selEDCItem=kwargs['edc'],clientid=kwargs['clientid'])
      
      intrpt.get_apikey()

      funname = 'EDC_NET_'+ fab.split("_")[0]
      intrpt.set_linkpage(funname)
      data = intrpt.request_api()
      cls.url = intrpt.qurl
      cls.apikey = intrpt.apikey
      return data


    def save_clientdatastore():
      # cds = ClientDataStore()
      pass
