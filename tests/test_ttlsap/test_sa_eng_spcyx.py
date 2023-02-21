from ttlsap.sa_eng_spcyx import SpcYxApi

def test_sa_eng_spcyx():
  nameddata = '/ds/eng/spcyx'
  start_time = '20220802080000'
  end_time = '20221222170000' 
  run_mode = 'N' 
  owner_code = 'CRN0' 
  peqpt = 'TLCD0300'
  fab = "TFT7"
  proc_id = "438N"
  item = "MB_X"
  prod = "TJDF40XK"
  recipe = "DF40XK_A5_4_254A"
  pproc_id = "4300"
  client_id = "eng"


  
  spcyx = SpcYxApi(nd=nameddata,fab=fab,proc_id=proc_id,item=item,prod=prod,recipe=recipe,pproc_id=pproc_id,start_time=start_time,
                end_time=end_time,run_mode=run_mode, owner_code= owner_code, peqpt=peqpt,clientid=client_id)
        
  endresult = spcyx.spcyxbytime()
  assert endresult["status"] == 200

  saveresult = spcyx.save_clientdatastore(asciifilename=True)
  assert saveresult["status"] == 200
