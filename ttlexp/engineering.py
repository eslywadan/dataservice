from datetime import date
from distutils.log import Log
import string
from xmlrpc.client import boolean
from flask import Blueprint,request
from flask_restx import Api, Resource, fields, reqparse
import json
from tools.response_handler import *
from tools.request_handler import check_and_log as verified_token 
from ttlsap.sa_eng import EdcRawApi
from taskman.celerytask import worker, async_edcrawbytime, async_spcyxbytime
from celery.result import AsyncResult

from ttlsap.sa_eng_spcyx import SpcYxApi
from tools.response_handler import InvalidUsage
from tools.celery_oper import *
from ttlsap.sa_eng_spcyx import SpcYxApi
from tools.response_handler import InvalidUsage

eng_bd = Blueprint('eng_api', __name__)
eng_api = Api(eng_bd)

edcrawapi = EdcRawApi()

@eng_bd.route('/hello/')
def hello():
	return "Hello from ENG Page"

edc_parser = eng_api.parser()
edc_parser.add_argument('start_time', type=str,  help='Required start time by date,ex:20220114140000')
edc_parser.add_argument('end_time', type=str, help='Required end time by date,ex:20220114160000')
# edc_net_parser.add_argument('grp_id', type=str, help='Optional, data provided only for specified glass id')
#edc_parser.add_argument('nowait', type=str, 
#    help='Required, If not true, wait on line till the data is responsed. if true, get the order id and retrieve the data by order id latter')
edc_parser.add_argument('token', type=str, help='Optional token')
@eng_api.route('/edc/edcRawByTime/<string:fab>/<string:equip>/<string:sub_equip>/items/<string:items>', methods=['GET'])
class Edc(Resource):
    @eng_api.doc('EDC NDE')
    @eng_api.expect(edc_parser)

    def get(self, fab, equip, sub_equip, items):
        chk_perm = verified_token(ignore_token=False)
        if chk_perm["status"] is not True:  return chk_perm["error_msg"]

        client_id = chk_perm["client_id"]
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        # sub_equip = request.args.get('sub_equip')

        Logger.log(f"full_path: {request.full_path}")
        Logger.log(f"url : {request.url}")
        Logger.log(f"path: {request.path}")
        Logger.log(f"query_string: {request.query_string}")
        saved_filename= f"{request.full_path}.json"
        
        #nowait = request.args.get('nowait')
        #Logger.log(f"edcraw nowait flag:{nowait}")

        #if nowait != 'true':
        return self.wait_online(fab=fab,equip=equip,edc=items,start_time=start_time,
                end_time=end_time,sub_eq=sub_equip,grp_id='',clientid=client_id, saved_filename=saved_filename)
        
        #if nowait == 'true':
        #    return self.nowait_async(fab=fab,equip=equip,edc=items,start_time=start_time,
        #        end_time=end_time,sub_eq=sub_equip,grp_id='',clientid=client_id, saved_filename=saved_filename)

    def wait_online(self,**kwargs):
        # Check the remote worker
        data = []
        items = kwargs['edc']
        #worker_stat = submit_tasks_start(worker,'taskman.celerytask.edcnetbytime')
        #if 0 in worker_stat: # wait on-line user but cannot find the available remote worker 
        #Logger.log("Has not the avaialbe remote worker, executed locally")
        for item in items.split(","):
                data.append(edcrawapi.edcnetbytime(fab=kwargs["fab"],equip=kwargs["equip"],edc=item,start_time=kwargs["start_time"],
                end_time=kwargs["end_time"],sub_eq=kwargs["sub_eq"],grp_id='',clientid=kwargs["clientid"]))

        #if 1 in worker_stat: # wait on-line user has available remote worker
        #    Logger.log("Has the avaialbe remote worker, executed remote")
        #    receipts = {}
        #    i = 1
        #    for item in items.split(","):
        #        receipt = async_edcrawbytime(fab=kwargs["fab"],equip=kwargs["equip"],edc=item,start_time=kwargs["start_time"],
        #        end_time=kwargs["end_time"],sub_eq=kwargs["sub_eq"],grp_id='',clientid=kwargs["clientid"])
        #        receipts[i] = receipt
        #        i += 1

        #    timeout = receipts.__len__()*10
        #    async_res = chk_async_tasks(receipts, timeout)
        #    st = async_res['Success Task']
        #    Logger.log(st)
        #    if st.__len__() == receipts.__len__():
        #        Logger.log("requested items are all completed")
        #    if st.__len__() > 0 and st.__len__() < receipts.__len__():
        #        Logger.log("requested items are partially compelted")
            
        #    for tid in st:
        #        data.append(AsyncResult(st[tid], app=worker).result)

        return JSNResponse(data)

    def nowait_async(self,**kwargs):
        # Check the remote worker
        data = []
        items = kwargs['edc']
        worker_stat = submit_tasks_start(worker,'taskman.celerytask.edcrawbytime')
        if 0 in worker_stat: # wait on-line user but cannot find the available remote worker
            m1 =  "Has not the avaialbe remote worker, please use nowait=false"
            Logger.log(m1)
            return JSNResponse(m1)
        if 1 in worker_stat: # wait on-line user has available remote worker
            Logger.log("Has the avaialbe remote worker, executed remote")
            receipts = {}
            i = 1
            for item in items.split(","):
                receipt = async_edcrawbytime(fab=kwargs["fab"],equip=kwargs["equip"],edc=item,start_time=kwargs["start_time"],
                end_time=kwargs["end_time"],sub_eq=kwargs["sub_eq"],grp_id='',clientid=kwargs["clientid"], saved_filename=kwargs["saved_filename"])
                receipts[i] = receipt
                i += 1

        return JSNResponse(receipts)


edc_raw_parser = eng_api.parser()
edc_raw_parser.add_argument('start_time', type=str,  help='Required start time by date,ex:20220114140000')
edc_raw_parser.add_argument('end_time', type=str, help='Required end time by date,ex:20220114160000')
edc_raw_parser.add_argument('sub_equip', type=str, help='Optional if sub_equip is diff with equip,ex:PFRW0100')
# edc_parser.add_argument('grp_id', type=str, help='Optional, data provided only for specified glass id')
edc_raw_parser.add_argument('nowait', type=str, 
    help='Required, If not true, wait on line till the data is responsed. if true, get the order id and retrieve the data by order id latter')
edc_raw_parser.add_argument('token', type=str, help='Optional token')
@eng_api.route('/edcraw/<string:fab>/<string:equip>/items/<string:items>', methods=['GET'])
class EdcRaw(Resource):

    @eng_api.doc('EDC Raw NDE')
    @eng_api.expect(edc_raw_parser)
    
    # @eng_api.marshal_with(edcraw_model)
    def get(self, fab, equip, items):
        chk_perm = verified_token(ignore_token=False)
        if chk_perm["status"] is not True:  return chk_perm["error_mfg"]

        client_id = chk_perm["client_id"]
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        sub_equip = request.args.get('sub_equip')

        Logger.log(f"full_path: {request.full_path}")
        Logger.log(f"url : {request.url}")
        Logger.log(f"path: {request.path}")
        Logger.log(f"query_string: {request.query_string}")
 
        saved_filename= f"{request.full_path}.json"
        return self.wait_online(fab=fab,equip=equip,edc=items,start_time=start_time,
                end_time=end_time,sub_eq=sub_equip,grp_id='',clientid=client_id, saved_filename=saved_filename)
        
        nowait = request.args.get('nowait')
        Logger.log(f"edcraw nowait flag:{nowait}")

        if nowait != 'true':
            return self.wait_online(fab=fab,equip=equip,edc=items,start_time=start_time,
                end_time=end_time,sub_eq=sub_equip,grp_id='',clientid=client_id, saved_filename=saved_filename)
        
        if nowait == 'true':
            return self.nowait_async(fab=fab,equip=equip,edc=items,start_time=start_time,
                end_time=end_time,sub_eq=sub_equip,grp_id='',clientid=client_id, saved_filename=saved_filename)

    def wait_online(self,**kwargs):
        # Check the remote worker
        data = []
        items = kwargs['edc']
        worker_stat = submit_tasks_start(worker,'taskman.celerytask.edcrawbytime')
        if 0 in worker_stat: # wait on-line user but cannot find the available remote worker 
            Logger.log("Has not the avaialbe remote worker, executed locally")
            for item in items.split(","):
                data.append(edcrawapi.edcrawbytime(fab=kwargs["fab"],equip=kwargs["equip"],edc=item,start_time=kwargs["start_time"],
                end_time=kwargs["end_time"],sub_eq=kwargs["sub_eq"],grp_id=''))

        if 1 in worker_stat: # wait on-line user has available remote worker
            Logger.log("Has the avaialbe remote worker, executed remote")
            receipts = {}
            i = 1
            for item in items.split(","):
                receipt = async_edcrawbytime(fab=kwargs["fab"],equip=kwargs["equip"],edc=item,start_time=kwargs["start_time"],
                end_time=kwargs["end_time"],sub_eq=kwargs["sub_eq"],grp_id='',clientid=kwargs["clientid"], saved_filename=kwargs["saved_filename"])
                receipts[i] = receipt
                i += 1

            timeout = receipts.__len__()*10
            async_res = chk_async_tasks(receipts, timeout)
            st = async_res['Success Task']
            Logger.log(st)
            if st.__len__() == receipts.__len__():
                Logger.log("requested items are all completed")
            if st.__len__() > 0 and st.__len__() < receipts.__len__():
                Logger.log("requested items are partially compelted")
            
            for tid in st:
                data.append(AsyncResult(st[tid], app=worker).result)

        return JSNResponse(data)

    def nowait_async(self,**kwargs):
        # Check the remote worker
        data = []
        items = kwargs['edc']
        worker_stat = submit_tasks_start(worker,'taskman.celerytask.edcrawbytime')
        if 0 in worker_stat: # wait on-line user but cannot find the available remote worker
            m1 =  "Has not the avaialbe remote worker, please use nowait=false"
            Logger.log(m1)
            return JSNResponse(m1)
        if 1 in worker_stat: # wait on-line user has available remote worker
            Logger.log("Has the avaialbe remote worker, executed remote")
            receipts = {}
            i = 1
            for item in items.split(","):
                receipt = async_edcrawbytime(fab=kwargs["fab"],equip=kwargs["equip"],edc=item,start_time=kwargs["start_time"],
                end_time=kwargs["end_time"],sub_eq=kwargs["sub_eq"],grp_id='',clientid=kwargs["clientid"], saved_filename=kwargs["saved_filename"])
                receipts[i] = receipt
                i += 1

        return JSNResponse(receipts)


spcyx_parser = eng_api.parser()
spcyx_parser.add_argument('start_time', type=str,  help='Required start time by date,ex:20220114140000')
spcyx_parser.add_argument('end_time', type=str, help='Required end time by date,ex:20220114160000')
spcyx_parser.add_argument('run_mode', type=str, help='Required ex: Normal, Abnormal, etc')
spcyx_parser.add_argument('owner_code', type=str, help='Required ex: PROD, CRN0 etc')
spcyx_parser.add_argument('peqpt', type=str, help='Required, the Pre-Processing equipments')
spcyx_parser.add_argument('nowait', type=str, 
    help='Required, If not true, wait on line till the data is responsed. if true, get the order id and retrieve the data by order id latter')
spcyx_parser.add_argument('token', type=str, help='Optional token')
@eng_api.route('/spcyx/<string:fab>/<string:proc_id>/<string:item>/<string:prod>/<string:recipe>/<string:pproc_id>', methods=['GET'])
class SpcYx(Resource):
    @eng_api.doc('SPCYX NDE')
    @eng_api.expect(spcyx_parser)
    def get(sellf, fab, proc_id, item, prod, recipe, pproc_id):
        chk_perm = verified_token(ignore_token=False)
        if chk_perm["status"] is not True:  return chk_perm["error_mfg"]

        client_id = chk_perm["client_id"]
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        run_mode = request.args.get('run_mode')
        owner_code = request.args.get('owner_code')
        peqpt = request.args.get('peqpt')
        nameddata = "/ds/eng/spcyx"

        nowait = request.args.get('nowait')
        if nowait == 'true':
            Logger.log(f"spcyx nowait flag:{nowait}")
            return async_spcyxbytime(nd=nameddata,fab=fab,proc_id=proc_id,item=item,prod=prod,recipe=recipe,pproc_id=pproc_id,start_time=start_time,
                    end_time=end_time,run_mode=run_mode, owner_code= owner_code, peqpt=peqpt,clientid=client_id)
        else:
            spcyx = SpcYxApi(nd=nameddata,fab=fab,proc_id=proc_id,item=item,prod=prod,recipe=recipe,pproc_id=pproc_id,start_time=start_time,
                    end_time=end_time,run_mode=run_mode, owner_code= owner_code, peqpt=peqpt,clientid=client_id)
            
            endresult = spcyx.spcyxbytime()
            if endresult["status"] == 200:
                resp = spcyx.save_clientdatastore()
                #resp = spcyx.save_spcyxdata(asciifilename=False)
                #resp = spcyx.save_spcyxdata(asciifilename=True)
                return JSNResponse( resp )
            else:
                return InvalidUsage(endresult)

    def wait_online(self,**kwargs):
        # Check the remote worker
        data = []
        items = kwargs['edc']
        worker_stat = submit_tasks_start(worker,'taskman.celerytask.edcrnetbytime')
        if 0 in worker_stat: # wait on-line user but cannot find the available remote worker 
            Logger.log("Has not the avaialbe remote worker, executed locally")
            for item in items.split(","):
                data.append(edcrawapi.edcnetbytime(fab=kwargs["fab"],equip=kwargs["equip"],edc=item,start_time=kwargs["start_time"],
                end_time=kwargs["end_time"],sub_eq=kwargs["sub_eq"],grp_id=''))

        if 1 in worker_stat: # wait on-line user has available remote worker
            Logger.log("Has the avaialbe remote worker, executed remote")
            receipts = {}
            i = 1
            for item in items.split(","):
                receipt = async_edcrawbytime(fab=kwargs["fab"],equip=kwargs["equip"],edc=item,start_time=kwargs["start_time"],
                end_time=kwargs["end_time"],sub_eq=kwargs["sub_eq"],grp_id='',clientid=kwargs["clientid"], saved_filename=kwargs["saved_filename"])
                receipts[i] = receipt
                i += 1

            timeout = receipts.__len__()*10
            async_res = chk_async_tasks(receipts, timeout)
            st = async_res['Success Task']
            Logger.log(st)
            if st.__len__() == receipts.__len__():
                Logger.log("requested items are all completed")
            if st.__len__() > 0 and st.__len__() < receipts.__len__():
                Logger.log("requested items are partially compelted")
            
            for tid in st:
                data.append(AsyncResult(st[tid], app=worker).result)

        return JSNResponse(data)

    def nowait_async(self,**kwargs):
        # Check the remote worker
        data = []
        items = kwargs['edc']
        worker_stat = submit_tasks_start(worker,'taskman.celerytask.edcrawbytime')
        if 0 in worker_stat: # wait on-line user but cannot find the available remote worker
            m1 =  "Has not the avaialbe remote worker, please use nowait=false"
            Logger.log(m1)
            return JSNResponse(m1)
        if 1 in worker_stat: # wait on-line user has available remote worker
            Logger.log("Has the avaialbe remote worker, executed remote")
            receipts = {}
            i = 1
            for item in items.split(","):
                receipt = async_edcrawbytime(fab=kwargs["fab"],equip=kwargs["equip"],edc=item,start_time=kwargs["start_time"],
                end_time=kwargs["end_time"],sub_eq=kwargs["sub_eq"],grp_id='',clientid=kwargs["clientid"], saved_filename=kwargs["saved_filename"])
                receipts[i] = receipt
                i += 1

        return JSNResponse(receipts)
