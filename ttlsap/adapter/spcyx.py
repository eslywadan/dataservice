from datetime import datetime, timedelta
from tools.redis_db import RedisDb
from tools.logger import Logger
from tools.general_fun import add_sql
from dbtools.db_connection import DbConnection as dbc
<<<<<<< HEAD
from dbtools.pddfread import read_query
=======
>>>>>>> 92cb12d (add innodrive and test about spcyx)
import pandas as pd
import numpy as np
import traceback
import os


def get_spcyx_data(info,redis_key):
<<<<<<< HEAD
    """return status code has 
        200 Sucess proceeded the request with content
        204 Sucess proceeded the request without content 
        503 Service Unavailable"""
=======
>>>>>>> 92cb12d (add innodrive and test about spcyx)
    try:
        #check_and_log(ignore_token=False,token = chart_list.token)
        redis = RedisDb.default()
        
        redis.set(redis_key,'start job',600)
        info = info.dict()
<<<<<<< HEAD
<<<<<<< HEAD
        Logger.log(info['chart_list'])
        if info['method']=='spc_chart_id':
            for chart in info['chart_list'].split(","):
=======
        print(info['chart_list'])
        Logger.log(info['chart_list'])
        if info['method']=='spc_chart_id':
            for chart in info['chart_list'].split(","):
                print(chart)
>>>>>>> 92cb12d (add innodrive and test about spcyx)
=======
        Logger.log(info['chart_list'])
        if info['method']=='spc_chart_id':
            for chart in info['chart_list'].split(","):
>>>>>>> 87bde97 (1.innodrive connect 2.spcyx data service)
                Logger.log(chart)
            info['chart_list'] = ",".join([f"'{chart.strip()}'" for chart in info['chart_list'].split(",")])
            sql_chart_id_part = f" and spc_chart_id in ({info['chart_list']})"
        else:
            sql_chart_id_part=''
    
        sql_get_spc_data='''select a.gls_id as GLS_ID,equip_id,prod_id,opra_id,pv_equip_id,pv_opra_id,owner_cd,prodn_dttm,equip_run_mode_cd,
case when substr(spc_chart_type_cd,1,2)='XX' then x_meas else avg_meas end as avg_meas,ucl1_meas,cl1_meas,lcl1_meas 
 from pdata_eda.MEA_SPC_{fab}_PARA  a
 join pdata_eda.MEA_SPC_{fab}_gls g
 on a.gls_id=g.gls_id
 and a.spc_seq_num=g.spc_seq_num
 where prodn_dttm between '{start_dttm}' and  '{end_dttm}' 
'''     
        sql_get_spc_data = sql_get_spc_data.format_map(info)
        sql_get_spc_data = sql_get_spc_data + sql_chart_id_part
        sql_get_spc_data = add_sql(sql_get_spc_data,"in",info["product"],'prod_id')
        sql_get_spc_data = add_sql(sql_get_spc_data,"in",info["pproc_id"],'PV_OPRA_ID')
        sql_get_spc_data = add_sql(sql_get_spc_data,"in",info["precipe_id"],'PV_RECIPE_ID')
        sql_get_spc_data = add_sql(sql_get_spc_data,"=",info["peqpt_id"],'PV_EQUIP_ID' )
        sql_get_spc_data = add_sql(sql_get_spc_data,"=",info["owner_code"],'owner_cd' )
        sql_get_spc_data = add_sql(sql_get_spc_data,"=",info["run_mode"],'equip_run_mode_cd' )
        if info['method']!='spc_chart_id':
            sql_get_spc_data = add_sql(sql_get_spc_data,"=",info["spc_item_id"],'spc_item_id')
            sql_get_spc_data = add_sql(sql_get_spc_data,"in",info["proc_id"],'OPRA_ID')
        sql_get_spc_data = sql_get_spc_data + " and oos_ind<>'Y' and substr(spc_chart_type_cd,1,2) in ('AG','XX')"

        
        redis.set(redis_key,'get spc data',600)
        conn_gp = dbc.edw_gp()
        spc_data = pd.read_sql(sql_get_spc_data,conn_gp)
        conn_gp.close()
        Logger.log(f"Describe spc_data: raw from gp {spc_data}")
        cols = [col.upper() for col in spc_data.columns]
        spc_data.columns = cols
        redis.set(redis_key,'get edc_item list',600)
        
        if spc_data.shape[0]==0:
            redis.set(redis_key,'no spc_data',600)
<<<<<<< HEAD
            
            return {"status":204,'message':'no spc data'}
=======
            return {'message':'no_data'}
        print("spc_data get done")
>>>>>>> 92cb12d (add innodrive and test about spcyx)

        if info["peqpt_id"]=='all':
            info["peqpt_id"] = spc_data.PV_EQUIP_ID[0]
        
        temp_peqpt_id = info['peqpt_id'].strip("0")
        
        sql_get_item_list = '''SELECT distinct EDC_ITEM_NAME FROM PEDAMART.DIM_KFM_EDC_ITEM where site='{fab}' 
                                and EQPT_ID LIKE '{peqpt_id}%' '''.format(fab=info['fab'],peqpt_id=temp_peqpt_id)

        sql_get_eqpt_list = '''SELECT distinct eqpt_id FROM PEDAMART.DIM_KFM_EDC_ITEM where site='{fab}' 
                                and EQPT_ID LIKE '{peqpt_id}%' '''.format(fab=info['fab'],peqpt_id=temp_peqpt_id)
        
<<<<<<< HEAD
        #hbase = dbc.cdp_hbase()
        #item_list = pd.read_sql(sql_get_item_list,hbase)
        #eqpt_list = pd.read_sql(sql_get_eqpt_list,hbase)

        phoenix = dbc.cdp_phoenix()
        item_list = read_query(sql_get_item_list,phoenix)
        eqpt_list = read_query(sql_get_eqpt_list,phoenix)
        Logger.log(f"get item_list data by sql {sql_get_item_list} from phoenix conn {phoenix}")
        #Logger.log(f"result item_list data {item_list}")
        Logger.log(f"get eqpt_list data by sql {sql_get_eqpt_list} from hbase conn {phoenix}")
        #Logger.log(f"result eqpt_list data {eqpt_list}")


=======
        hbase = dbc.cdp_hbase()
        item_list = pd.read_sql(sql_get_item_list,hbase)
        eqpt_list = pd.read_sql(sql_get_eqpt_list,hbase)
>>>>>>> 92cb12d (add innodrive and test about spcyx)
        eqpt_list = eqpt_list.EQPT_ID.tolist()
        max_len = max([len(t) for t in eqpt_list])
        count=0
        while True:
            x = [t[0:max_len-count] for t in eqpt_list]
            if np.unique(x).shape[0]==1:
                break
            count+=1
        line_eqpt = x[0]
        substr_count = str(max_len - count)
        redis.set(redis_key,'get edc data',600)
        item_sql_part = ",".join([f'"D"."{item}" VARCHAR' for item in item_list.EDC_ITEM_NAME]) #in ({eqpt_list})
        gls_sql_part = ",".join([f"'{gls}'" for gls in spc_data.GLS_ID])
        sql_get_edc_data = "select * FROM PDATA_EDA.MEA_EDC_{fab} ({item_sql_part}) where gls_id in ({gls_sql_part}) and substr(eqpt_id,1,{substr_count}) = substr('{eqpt_list}',1,{substr_count})"
        sql_get_edc_data = sql_get_edc_data.format(fab=info['fab'],item_sql_part = item_sql_part ,gls_sql_part=gls_sql_part,eqpt_list=line_eqpt,substr_count=substr_count)
<<<<<<< HEAD
        # edc_data = pd.read_sql(sql_get_edc_data,hbase)
        edc_data = read_query(sql_get_edc_data,phoenix)
        Logger.log(f"get edc data by sql {sql_get_edc_data} from phoenix conn {phoenix}")

=======
        edc_data = pd.read_sql(sql_get_edc_data,hbase)
>>>>>>> 92cb12d (add innodrive and test about spcyx)
        redis.set(redis_key,'creat all columns',600)

        for item in item_list.EDC_ITEM_NAME:
            temp = edc_data[item]
            try:
                temp = temp.astype(float)
                is_str = False
            except:
                is_str = True
            if temp.isna().all() or temp.isna().all() or is_str:
                edc_data = edc_data.drop([item], axis=1)
            else:
                temp[temp.isna()]=None
                edc_data[item] = temp
        
        edc_data = edc_data.where(pd.notnull(edc_data), None)
        #合併2份資料
        redis.set(redis_key,'merge spc_data with edc_data',600)
        temp = item_list['EDC_ITEM_NAME'].tolist()
        normal_edc_items =  [col for col in edc_data.columns if col in temp]
        eqpts = edc_data.EQPT_ID.sort_values().unique().tolist()
        all_items ={}
        for eqpt in eqpts:
            for item in normal_edc_items:
                all_items[f"{eqpt}_{item}"]=""
<<<<<<< HEAD

=======
>>>>>>> 92cb12d (add innodrive and test about spcyx)
        temp_df = pd.DataFrame(all_items,index=spc_data.index)
        all_cols = spc_data.columns.tolist()+[k for k in all_items.keys()]
        spc_data = spc_data.assign(**temp_df)
        spc_data = spc_data[all_cols]
<<<<<<< HEAD


=======
>>>>>>> 92cb12d (add innodrive and test about spcyx)
        count = 0
        ans_spc_data = spc_data.loc[[False]*spc_data.shape[0]] #加速合併速度  整理完單筆spc 先append至此
        for gls in spc_data.GLS_ID:
            count = count + 1
            redis.set(redis_key,f'merge spc_data with edc_data {str(count)}/{str(spc_data.shape[0] )}',600)
            temp_edc_data = edc_data.loc[edc_data.GLS_ID==gls]
            temp_spc_data=spc_data.loc[spc_data.GLS_ID==gls]
            for gro,row in temp_edc_data.groupby(['EQPT_ID','GLS_ID']):
                if row.shape[0]>1:
                    delta = []
                    for t in row.TXN_DTTM:
<<<<<<< HEAD
<<<<<<< HEAD
                        # print(temp_spc_data.PRODN_DTTM)
                        # Logger.log(f"type of t {type(t)}:{t} to str {str(t)}")
                        if type(t) is not str: t = str(t)
=======
                        print(temp_spc_data.PRODN_DTTM)
>>>>>>> 92cb12d (add innodrive and test about spcyx)
=======
                        # print(temp_spc_data.PRODN_DTTM)
>>>>>>> 87bde97 (1.innodrive connect 2.spcyx data service)
                        try:
                            temp_delta = (datetime.strptime(t,"%Y-%m-%d %H:%M:%S")-datetime.strptime(temp_spc_data.PRODN_DTTM.tolist()[0],"%Y-%m-%d %H:%M:%S")).total_seconds()
                        except:
                            temp_delta = (datetime.strptime(t,"%Y-%m-%d %H:%M:%S")-temp_spc_data.PRODN_DTTM.tolist()[0]).total_seconds()
                        delta.append(abs(temp_delta))
                    drop_ros = []
                    for n,de in zip(range(len(delta)),delta):
                        if de!=min(delta):
                            drop_ros.append(row.index[n])
                    temp_edc_data = temp_edc_data.drop(drop_ros,axis=0)
            for index,row in temp_edc_data.iterrows():
                for item in normal_edc_items:
                    temp_spc_data[f"{row.EQPT_ID}_{item}"]=row[item]
            ans_spc_data = ans_spc_data.append( temp_spc_data,ignore_index=True)
        spc_data = ans_spc_data

<<<<<<< HEAD
        # Logger.log(f"Describe spc_data: get edc_item list {spc_data}")
=======
        Logger.log(f"Describe spc_data: get edc_item list {spc_data}")
>>>>>>> 92cb12d (add innodrive and test about spcyx)

        empty_col = []
        for col in spc_data.columns:
            if ((spc_data[col].isna()) | (spc_data[col]=="")).all():
                empty_col.append(col)

        spc_data = spc_data.drop(empty_col, axis=1)
        redis.set(redis_key,'data convert to csv file',600)
<<<<<<< HEAD
        
        filename = f"{redis_key.decode('ascii')}.csv"
        filepath = os.path.join("ext",filename)
        spc_data.to_csv(filepath,index=False)
        # Logger.log(f"Describe spc data: Done {spc_data}")
        redis.set(redis_key,'done',60000)

        return {"status":200,"message":"done","filename":filename,"filepath":filepath}

=======
        filename = f"{redis_key.decode('ascii')}.csv"
        filepath = os.path.join("ext",filename)
        spc_data.to_csv(filepath,index=False)
        Logger.log(f"Describe spc data: Done {spc_data}")
        redis.set(redis_key,'done',60000)

<<<<<<< HEAD
        return {"message":"done"}
>>>>>>> 92cb12d (add innodrive and test about spcyx)
=======
        return {"message":"done","filename":filename,"filepath":filepath}

>>>>>>> 87bde97 (1.innodrive connect 2.spcyx data service)
    except Exception as e:
        redis.set(redis_key,'error',600)
        Logger.log(traceback.format_exc())