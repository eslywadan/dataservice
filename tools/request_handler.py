from logging.config import valid_ident
from flask import request, render_template
import ttlsap.fab_proc as fab_proc
import ttlsap.edc_data as edc_data
import ttlsap.edc_dim as edc_dim
import ttlsap.spc_dim as spc_dim
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tools.redis_db import RedisDb, CacheType
from tools.logger import Logger
import tools.reset_config as reset_config
from tools.cache_key import get_cache_key
from tools.response_handler import * 
from grpc_cust.clientapival_client import get_clientapikey, get_verified_apikey
from tools.response_handler import InvalidUsage


def process_login(**kwargs):


    if "clientId" in request.headers:
        client_id = request.headers["clientId"]
    else:
        client_id = request.args.get('clientId')

    if "password" in request.headers:
        password = request.headers["password"]
    else:
        password = request.args.get('password')

    apikey = get_clientapikey(client_id, password)

    if apikey.expiry == "1900-01-01":
        Logger.log(f"Client id {client_id} fail on process_login")
        return JSNError(f"Client Id {client_id} or password {password} is not correct.",status_code=401)
    
    Logger.log(f'Issue request: {client_id}, {request.method}, {request.url}')
    return JSNResponse(apikey.apikey)


def dummy_check_and_log():
    return  {"status":True,"apikey":"given_token"}


def check_and_log(ignore_token=False):
    if ignore_token:
        Logger.log(f'Issue request: {request.method}, {request.url}')
        return True

    if "apikey" in request.headers: 
        given_token = request.headers["apikey"]

    if request.args.get('token'):
        given_token = request.args.get('token')

    if given_token is not None:
        token_info =  get_verified_apikey(given_token)
        client_type = token_info.assertion.split(":")[1]

    if client_type == "BLOCK":
        return {"status":False,"error_msg":InvalidUsage("Given token has found the client is blocked from requesting data services",status_code=401)}

    if token_info.apikey == given_token:
        if token_info.assertion is not None:
            registry = token_info.assertion.split(":")[2]
            granted = validate_ds_permission(registry,request.url)
            Logger.log(f'Issue request: @{given_token}, {request.method}, {request.url}, {token_info.assertion}')
            if granted == "Permit":
                client_id = token_info.assertion.split(":")[0]
                client_prev = token_info.assertion.split(":")[2]
                return {"status":True,"apikey":given_token, "client_id":client_id}
            else:
                return {"status":False,"error_msg":InvalidUsage("Given token has not the permission for requesting data services",status_code=403)}

    Logger.log(f'Deny request: {request.method}, {request.url}')
    return {"status":False,"error_msg":InvalidUsage("Given token is not correct!",status_code=401)}


def validate_ds_permission(registry, url):

    nde =url.partition("/ds")[2]
    permit = []
    if len(registry.strip())==0:  return "No Permit"
    for reg in registry.split(","): 
        if reg.startswith("-") and nde.startswith(reg.partition("-")[2]):
            # Negative element, match pattern is not allowed
            permit.append(False)

        if not reg.startswith("-") and nde.startswith(reg):
            permit.append(True)

    if permit.__contains__(False) or permit.__len__() == 0:
        return "No Permit"
    else:
        return "Permit"


#先檢查cache，有則回傳，沒有則建立
def process_req_fab_proc():
    if not check_and_log()["status"]:
        return JSNError("Token is missing or token is not correct. Please call Login API to get a new token.")
    
    cache_type = RedisDb.cache_type()
    if cache_type == CacheType.AUTO:
        list = find_cache()
        if list is None:
            list = get_fab_proc()
            set_cache(list)
    elif cache_type == CacheType.READONLY:
        list = find_cache()
    elif cache_type == CacheType.IGNORE:
        list = get_fab_proc()
    elif cache_type == CacheType.RENEW:
        list = get_fab_proc()
        set_cache(list)
    elif cache_type == CacheType.BUILD:
        list = get_fab_proc()
        set_cache(list)
        list = []

    return JSNResponse(list)


def get_fab_proc():
    if request.endpoint == 'get_fab_list':
        list = fab_proc.get_fab_list()
    else:
        fab = request.args.get('fab')
        list = fab_proc.get_proc_list(fab)

    return list


#依據cache type存取資料
def process_req(fab=None, process=None):
    if not check_and_log()["status"]:
        return JSNError("Token is missing or token is not correct. Please call login API to get a new token.")
    
    cache_type = get_cache_type()
    if cache_type == CacheType.AUTO:
        list = find_cache()
        if list is None:
            list = get_list_from_db(fab, process)
            set_cache(list)
    elif cache_type == CacheType.READONLY:
        list = find_cache()
        if list is None: list = []
    elif cache_type == CacheType.IGNORE:
        list = get_list_from_db(fab, process)
    elif cache_type == CacheType.RENEW:
        list = get_list_from_db(fab, process)
        set_cache(list)
    elif cache_type == CacheType.BUILD:
        list = get_list_from_db(fab, process)
        set_cache(list)
        list = [0]*len(list)

    return JSNResponse(list)


def get_list_from_db(fab, process):
    func_name = request.endpoint
    args = get_args()
    if 'spc' in func_name:
        func = getattr(spc_dim, func_name)
    else:
        func = getattr(edc_dim, func_name)

    list = func(fab, process, **args)
    return list


#不使用cache
def process_req_no_cache(fab=None, process=None, equipment=None):
    if not check_and_log()["status"]:
        return JSNError("Token is missing or token is not correct. Please call login API to get a new token.")
    
    func_name = request.endpoint
    args = get_args()
    func = getattr(edc_data, func_name)

    if equipment: rv = func(fab, equipment=equipment, **args)   #沒有process
    else: rv = func(fab, process=process, **args)               #equipment在args

    return JSNResponse(rv)


def process_req_ui():
    check_and_log(ignore_token=True)

    if request.endpoint == 'get_main_menu':
        return render_template('default.html', description='Main Functions:',  action_url='/reset-config', action_name='Reset Config')

    if request.endpoint == 'reset_config':
        reset_config.reset_config()
        return render_template('default.html', message='Config refreshed!',  action_url='/home', action_name='Main Menu')





#region 讀寫cache
def find_cache():
    key = get_cache_key(request.full_path)
    redis = RedisDb.default()
    list = redis.get(key)
    if list is None: return None
    if list == '': return []
    return list.split(',')


def set_cache(list):
    try:
        key = get_cache_key(request.full_path)
        redis = RedisDb.default()
        expiry_hours=get_cache_expiry_hours()
        redis.set(key, ','.join(list), expiry_hours=expiry_hours)
    except Exception as err:
        logger = Logger.default()
        logger.error(f'"{err.args[0]}" on set_cache() in request_handler.py', exc_info=True)


#endregion


#region 取得查詢參數裡的cache選項

#優先採用request.headers裡的cacheType，若沒有或無法解析再使用系統的cache_type
def get_cache_type():
    if "cacheType" in request.headers: 
        try:
            return CacheType[request.headers["cacheType"]]
        except:
            pass

    #200514:查詢eqpt，只使用cache，不查詢資料庫，即使當月
    #200515:只限CNVR
    #elif request.endpoint == "get_eqpt_list" and request.view_args['process'] == 'CNVR':
    #200520:不限CNVR
    elif request.endpoint == "get_eqpt_list" and "month" in request.args:
        return CacheType.READONLY

    return RedisDb.cache_type()

#採用request.headers裡的expiryHours，若沒有或無法解析回傳None(會使用預設的 expiry_hours)，若小於等於0則cache不會timeout
def get_cache_expiry_hours():
    if "expiryHours" in request.headers: 
        try:
            return float(request.headers["expiryHours"])
        except:
            pass
    
    #ch200513:如果查詢的區間是by month且是當月，非eqpt清單，cache一天
    elif 'month' in request.args and request.args['month'] == datetime.today().strftime('%Y-%m') and request.endpoint != "get_eqpt_list":
        return 24.0

    return None

#endregion


#將查詢參數轉為一般Dictionary，並做參數轉換，與日期預處理
def get_args():
    dict = request.args.to_dict()

    #name mapping
    if "ownerCode" in dict: dict["owner_code"] = dict.pop("ownerCode")
    if "chamberCode" in dict: dict["chamber_code"] = dict.pop("chamberCode")
    if "withTypeCode" in dict: dict["with_type_code"] = dict.pop("withTypeCode")=="true"
    if "buildSqlOnly" in dict: dict["build_sql_only"] = dict.pop("buildSqlOnly")=="true"
    if "dataShapeWide" in dict: dict["data_shape_wide"] = dict.pop("dataShapeWide")=="true"
    if "prfxOpraEqpt" in dict: dict["prfx_opra_eqpt"] = dict.pop("prfxOpraEqpt")=="true"
    if "spcOperation" in dict: dict["spc_operation"] = dict.pop("spcOperation")
    if "measureType" in dict: dict["measure_type"] = int(dict.pop("measureType"))

    #posted data
    if request.method == 'POST':
        posted = request.get_json()
        if posted:
            if "EdcItems" in posted: dict["edc_items"] = posted["EdcItems"]
            if "SpcItems" in posted: dict["spc_items"] = posted["SpcItems"]


    #決定資料的日期區間start and end
    if "month" in dict:
        month = dict.pop("month") # eg. '2020-04'
        start_date = datetime.strptime(month, "%Y-%m") # eg. datetime.datetime(2020, 4, 1, 0, 0)
    elif "start" in dict:
        start = dict.pop("start")
        start_date = datetime.strptime(start, "%Y-%m-%d") if len(start) >= 8 else datetime.strptime(start, "%Y-%m")
    else:
        start_date = datetime.today()

    if "end" in dict:
        end = dict.pop("end")
        end_date = datetime.strptime(end, "%Y-%m-%d") if len(end) >= 8 else datetime.strptime(end, "%Y-%m")
        if end_date - start_date > timedelta(31):
            end_date = start_date + relativedelta(months = 1) - relativedelta(days = 1)
    else:
        end_date = start_date + relativedelta(months = 1) - relativedelta(days = 1)

    #ch200514:get_edc_spc_data要多給spc_end參數，spc資料可能落後edc二~三個月
    if "spc_operation" in dict and "operation" in dict:
        spc_end_date = start_date + relativedelta(months = 3)
        dict["spc_end"] = spc_end_date.strftime("%Y-%m-%d")

    dict["start"] = start_date.strftime("%Y-%m-%d")
    dict["end"] = end_date.strftime("%Y-%m-%d")

    return dict


