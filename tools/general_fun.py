from tools.logger import Logger
from flask import Response
from tools.redis_db import RedisDb
import json
from datetime import datetime, timedelta
import random

def add_sql(sql,mode,values=None,col=None):
    if values == "all" or values is None:
        return sql
    if mode=="in":
        values = ",".join([f"'{value}'" for value in values.split(",")])
        sql=sql+f" and {col} in ({values})"
    else:
        sql = sql + f" and {col}='{values}'"
    return sql

def get_menu_measure_sql(info):
    sql = '''
        select OPRA_ID,spc_item_id from pdata_eda.MEA_SPC_{fab}_PARA  a
            join pdata_eda.MEA_SPC_{fab}_gls g
            on a.gls_id=g.gls_id
            and a.spc_seq_num=g.spc_seq_num
            WHERE g.prodn_dttm BETWEEN  '{start_dttm}' and  '{end_dttm}' 
    '''
    sql = sql.format_map(info)
    sql = add_sql(sql,"in",info["product"],'prod_id')
    sql = add_sql(sql,"in",info["pproc_id"],'PV_OPRA_ID')
    sql = add_sql(sql,"in",info["precipe_id"],'PV_RECIPE_ID')
    sql = add_sql(sql,"=",info["peqpt_id"],'PV_EQUIP_ID' )
    sql = add_sql(sql,"=",info["owner_code"],'owner_cd' )
    sql = add_sql(sql,"=",info["run_mode"],'equip_run_mode_cd' )

    return sql

def get_menu_sql(target,fab,chart_list,start,end,method):
    

    sql = f''' SELECT {target} FROM pdata_eda.MEA_SPC_{fab}_PARA  a
            join pdata_eda.MEA_SPC_{fab}_gls g
            on a.gls_id=g.gls_id
            and a.spc_seq_num=g.spc_seq_num
            WHERE g.prodn_dttm BETWEEN  '{start}' AND '{end}' 
            '''
    if method=='spc_chart_id':
        chart_list =[f"'{chart}'" for chart in chart_list]
        chart_list = ",".join(chart_list)
        sql = sql + f' and spc_chart_id in ({chart_list})'
    return sql
#繼承Response，預設status code:200，預設mimetype:application/json
class JSNResponse(Response):
    def __init__(self, payload,json_format=False, status_code=200):
        if json_format:
            Response.__init__(self, payload)
        else:
            Response.__init__(self, json.dumps(payload))
        self.status_code = status_code
        self.media_type = 'application/json'

        Logger.log(f'End request: {status_code}')


#region 讀寫cache
def find_cache_json(key):
    redis = RedisDb.default()
    list = redis.get(key)
    print(list)
    if list is None: return None
    if list == '': return []
    return json.loads(list)

def set_cache_json(key,list,expiry_secs=None):
    try:
        if type(list) !=str:
            list = json.dumps(list, ensure_ascii=False)
        redis = RedisDb.default()
        if expiry_secs is None:
            expiry_secs = 24 *3600
        redis.set(key,list, expiry_secs=expiry_secs)
    except Exception as err:
        logger = Logger.default()
        logger.error(f'"{err.args[0]}" on set_cache() in request_handler.py', exc_info=True)

def find_cache(key):
    redis = RedisDb.default()
    list = redis.get(key)
    if list is None: return None
    if list == '': return []
    return list.split(',')

def set_cache(key,list,expiry_secs=None):
    try:
        redis = RedisDb.default()
        if expiry_secs is None:
            expiry_secs = 24 *3600
        redis.set(key, ','.join(list), expiry_secs=expiry_secs)
    except Exception as err:
        logger = Logger.default()
        logger.error(f'"{err.args[0]}" on set_cache() in request_handler.py', exc_info=True)

def made_ticket_no(count):
    basic = (datetime.now()+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S.")
    time = [basic + str(i).zfill(6)for i in range(count)]
    ran = [str(random.uniform(0,1))[3:9] for i in range(count)]
    return [f"{a}_UI{b}" for a,b in zip(time,ran)]

def series2dic(series:str):
    """convert the input series to dic type
       the series is seperated by ','
    """
    templ = series.split(',')
    res = {i:templ[i] for i in range(0, len(templ),1)}
    return res