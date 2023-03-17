from datetime import datetime, timedelta
from pickle import TRUE
from tools.redis_db import RedisDb
from tools.logger import Logger
from tools.general_fun import add_sql
from dbtools.db_connection import DbConnection as dbc
from dbtools.pddfread import read_query
from dbtools.sql_buffer import SqlBuffer
from model.model import spc_data_info
import pandas as pd
import numpy as np
from tools.pandasext import PdExt
import traceback
import os


class SpcYx(SqlBuffer):
    concurrent_time_latency = 100 
    edc_rowkey = ['GLS_ID', 'EQPT_ID', 'RECIPE_ID', 'LOT_ID', 'PROD_ID', 'EC_CD', 'OWNER_CD', 'RECIPE_ID', 'OPRA_ID', 'CST_ID', 'PLANT_LOC_ID', 'LINE_EQPT_ID']
    edc_grpkey = ['GLS_ID', 'EQPT_ID', 'RECIPE_ID', 'LOT_ID', 'PROD_ID', 'EC_CD', 'OWNER_CD', 'RECIPE_ID', 'OPRA_ID', 'CST_ID', 'PLANT_LOC_ID', 'LINE_EQPT_ID', pd.Grouper(key="DATA_DTTM", freq="60s")]
    edc_join_key = ['GLS_ID', 'PROD_ID', 'OWNER_CD']
    spc_join_key = ['GLS_ID', 'PROD_ID', 'OWNER_CD']


    def __init__(self, info:spc_data_info, redis_key=None):
        self.info = info
        self.redis_key = redis_key
        self.switch_dbcode()
    

    def switch_dbcode(self):
        self.use_gp = True
        self.conn_db = "gp"
        gp_start_date = (datetime.now()-timedelta(days=180)).strftime('%Y-%m-01 00:00:00') #gp資料最舊日期
        self.use_gp = False if self.info.start_dttm < gp_start_date and self.info.fab not in ['T2','L2','F2','TT6','FT6','LT6'] else True
        self.conn_db = 'CDP' if self.info.start_dttm < gp_start_date and self.info.fab not in ['T2','L2','F2','TT6','FT6','LT6'] else 'gp'
        Logger.log(f"{self.__str__}:use {self.conn_db} for retreiving spc data")

    def gen_sql_chart_id_part(self):
        
        if self.info.method =='spc_chart_id':
            for chart in self.info.chart_list.split(","):
                Logger.log(chart)
            
            self.info.chart_list = ",".join([f"'{chart.strip()}'" for chart in self.info.chart_list.split(",")])
            self._sql_chart_id_part = f" and spc_chart_id in ({self.info.chart_list})"
        else:
            self._sql_chart_id_part=''
        Logger.log(f"{self.__str__}:gen_sql_chart_id_part {self._sql_chart_id_part} ")

    def gen_sql_get_spc_data(self):
        self.gen_sql_chart_id_part()
        self.info.val_cols = self.info.data_type.replace('avg',"case when substr(spc_chart_type_cd,1,2)='XX' then x_meas else avg_meas end as avg_meas")
        self.info.spc_chart_type_cd = ',substr(spc_chart_type_cd,1,2) as spc_chart_type_cd' if self.info.method=='spc_chart_id' else ''
        if self.use_gp  :
            sql_get_spc_data='''select a.{table_col} as GLS_ID,spc_chart_id,equip_id,prod_id,opra_id,pv_equip_id,pv_opra_id,PV_RECIPE_ID,owner_cd,prodn_dttm,equip_run_mode_cd,
                                ucl1_meas,cl1_meas,lcl1_meas{spc_chart_type_cd}
                                from pdata_eda.MEA_SPC_{fab}_PARA  a
                                join pdata_eda.MEA_SPC_{fab}_gls g
                                on a.{table_col}=g.{table_col}
                                and a.spc_seq_num=g.spc_seq_num
                                where prodn_dttm between '{start_dttm}' and  '{end_dttm}' 
                                '''    
        else:
            sql_get_spc_data = '''select a.{table_col} as GLS_ID,spc_chart_id,equip_id,prod_id,opra_id,pv_equip_id,pv_opra_id,PV_RECIPE_ID,owner_cd,prodn_dttm,equip_run_mode_cd,
                                ucl1_meas,cl1_meas,lcl1_meas {spc_chart_type_cd} from pdata_eda.MEA_SPC_{fab}_PARA  a where to_char(prodn_dttm) between '{start_dttm}' and  '{end_dttm}' 
                                '''
        if self.info.fab[0]=='L':
            self.info.table_col="pnl_id"
        else:
            self.info.table_col="gls_id"
        
        self.info.oos_sql ="oos_ind," if self.info.oos_filter.lower()=='false' else ''
        sql_get_spc_data = sql_get_spc_data.format_map(self.info.dict())
        sql_get_spc_data = sql_get_spc_data + self._sql_chart_id_part
        
        if self.info.method != 'spc_chart_id':
            sql_get_spc_data = add_sql(sql_get_spc_data,"=", self.info.spc_item_id,'spc_item_id')
            sql_get_spc_data = add_sql(sql_get_spc_data,"in", self.info.proc_id,'OPRA_ID')
            sql_get_spc_data = add_sql(sql_get_spc_data,"in", self.info.product,'prod_id')
            sql_get_spc_data = add_sql(sql_get_spc_data,"in", self.info.pproc_id,'PV_OPRA_ID')
            sql_get_spc_data = add_sql(sql_get_spc_data,"in", self.info.precipe_id,'PV_RECIPE_ID')
            sql_get_spc_data = add_sql(sql_get_spc_data,"=", self.info.peqpt_id,'PV_EQUIP_ID' )
            sql_get_spc_data = add_sql(sql_get_spc_data,"=", self.info.owner_code,'owner_cd' )
            sql_get_spc_data = add_sql(sql_get_spc_data,"=", self.info.run_mode,'equip_run_mode_cd' )
            sql_get_spc_data = sql_get_spc_data + " and substr(spc_chart_type_cd,1,2) in ('AG','XX')"
        if self.info.oos_filter.lower()=='true':
            sql_get_spc_data = sql_get_spc_data + " and oos_ind<>'Y'"

        self._sql_get_spc_data = sql_get_spc_data 
        Logger.log(f"{self.__str__}:gen_sql_get_spc_data {self._sql_get_spc_data} ")
        
    def get_spc_data(self):
        self.gen_sql_get_spc_data()
        print(f"using db: {self.conn_db} by sql {self._sql_get_spc_data}")
        if self.conn_db == "gp":
            conn_gp = dbc.edw_gp()
            self.spc_data = read_query(self._sql_get_spc_data,conn_gp)
            conn_gp.close()
        if self.conn_db == "CDP":
            conn_cdp = dbc.cdp_phoenix
            self.spc_data = read_query(self._sql_get_spc_data,conn_cdp())
        
        cols = [col.upper() for col in self.spc_data.columns]
        self.spc_data.columns = cols
        Logger.log(f"{self.__str__}:get_spc_data {self.spc_data.columns} ")

    def gen_sql_get_item_list(self,restrict_op=True):
        if restrict_op:self._sql_get_item_list = sql_get_item_list = '''SELECT distinct EDC_ITEM_NAME FROM PEDAMART.DIM_KFM_EDC_ITEM where site='{fab}' 
                                and EQPT_ID LIKE '{peqpt_id}%' and OPRA_ID='{pproc_id}' '''.format(fab=self.info.fab, peqpt_id=self.info.peqpt_id.strip("0"),pproc_id=self.info.pproc_id )

        else:self._sql_get_item_list = sql_get_item_list = '''SELECT distinct EDC_ITEM_NAME FROM PEDAMART.DIM_KFM_EDC_ITEM where site='{fab}' 
                                and EQPT_ID LIKE '{peqpt_id}%' '''.format(fab=self.info.fab, peqpt_id=self.info.peqpt_id.strip("0"))

    def get_item_list(self,restrict_op=True):
        self.gen_sql_get_item_list(restrict_op)
        phoenix = dbc.cdp_phoenix()
        self.item_list = read_query(self._sql_get_item_list,phoenix)
        phoenix.close()
        Logger.log(f"{self.__str__}:get_item_list {self.item_list} ")

    def gen_sql_get_items(self):
        self._sql_get_items = sql_get_items = '''SELECT * FROM PEDAMART.DIM_KFM_EDC_ITEM where site='{fab}' 
                                and EQPT_ID LIKE '{peqpt_id}%' '''.format(fab=self.info.fab, peqpt_id=self.info.peqpt_id.strip("0"))

    def get_items(self):
        self.gen_sql_get_items()
        phoenix = dbc.cdp_phoenix()
        self.items = read_query(self._sql_get_items,phoenix)
        phoenix.close()
        Logger.log(f"{self.__str__}:get_items {self.items} ")

    def gen_sql_get_eqpt_list(self):
        self._sql_get_eqpt_list = '''SELECT distinct eqpt_id FROM PEDAMART.DIM_KFM_EDC_ITEM where site='{fab}' 
                                and EQPT_ID LIKE '{peqpt_id}%' '''.format(fab=self.info.fab, peqpt_id=self.info.peqpt_id.strip("0"))

    def get_eqpt_list(self):
        self.gen_sql_get_eqpt_list()
        phoenix = dbc.cdp_phoenix()
        self.eqpt_list = read_query(self._sql_get_eqpt_list, phoenix)
        phoenix.close()
        Logger.log(f"{self.__str__}:get_eqpt_list {self.eqpt_list} ")

    def gen_sql_get_edc_data(self):
        eqpt_list = self.eqpt_list.EQPT_ID.tolist()
        max_len = max([len(t) for t in eqpt_list])
        count=0
        while True:
            x = [t[0:max_len-count] for t in eqpt_list]
            if np.unique(x).shape[0]==1:
                break
            count+=1
        line_eqpt = x[0]
        substr_count = str(max_len - count)
        item_sql_part = ",".join([f'"D"."{item}" VARCHAR' for item in self.item_list.EDC_ITEM_NAME]) #in ({eqpt_list})
        gls_sql_part = ",".join([f"'{gls}'" for gls in self.spc_data.GLS_ID])
        sql_get_edc_data = "select * FROM PDATA_EDA.MEA_EDC_{fab} ({item_sql_part}) where gls_id in ({gls_sql_part}) and substr(eqpt_id,1,{substr_count}) = substr('{eqpt_list}',1,{substr_count})"
        self._sql_get_edc_data = sql_get_edc_data.format(fab=self.info.fab,item_sql_part = item_sql_part ,gls_sql_part=gls_sql_part,eqpt_list=line_eqpt,substr_count=substr_count)

    def get_edc_data(self):
        self.gen_sql_get_edc_data()
        phoenix = dbc.cdp_phoenix()
        self.edc_data_raw = read_query(self._sql_get_edc_data, phoenix)
        phoenix.close()
        Logger.log(f"{self.__str__}:get_eqpt_list has row counts {self.edc_data_raw.count} ")

    def wrangle_edc_data(self,drop_all_na=True,fill_na=True):
        """More specifically, it will wrangle edc data by
        1. keyword: "drop_all_na" 
           Once the item's data contains all 'None' value, it will be removed by default
        2. keyword: "fillna_edc_data" 
           The same edc batch data may have two records due to the transaction latency even the same glass, the "fillna_edc_data" function will
           use groupby key to find the identical records and then fill the na for each other's value  
        3. keyword: "infer_edc_col_type"
            Except the column 'TXT_DTTM' and the column 'DATA_DTTM' will be recognized as datatime type on loading into dataframe when querying from source,
            others coulmns are 'object' type on the begining of data loading. It has annoying waring if doing numeric computation without specifying columns.
            thus, use the customized function to seperate the columns' type into 'num' & 'str', it is helpful on sucessing mungling steps
        4. keyword: "merge_edc_data"
            4-1 use groupby and agg("mean") to merge duplicated rows for columns with numeric type
            4-2 use groupby and agg("min") <or also available by "max"> to merge duplicate rows for columns with string type
            4-3 use concat to combine the data frame obtained by 4-1 & 4-2 and get the final edc_data
        """
        
        if drop_all_na: 
            edc_data_c0 = self.edc_data_raw.dropna(axis=1, how='all')
            removed_c_set = self.edc_data_raw.columns.difference(edc_data_c0.columns)
            Logger.log(f"Columns '{removed_c_set}' is checked all na and drop_all_na is {drop_all_na} thus be removed")
        else: edc_data_c0 = self.edc_data_raw
        
        Logger.log(f"{self.__str__}:wrangle_edc_data drop_all_na edc_data_c0")

        if fill_na:
            self.edc_data_c1 = SpcYx.fillna_edc_data(edc_data_c0)
            Logger.log(f"{self.__str__}:fillna_edc_data")
        self._edc_col_type = SpcYx.infer_edc_col_type(self.edc_data_c1, self.edc_rowkey)
        Logger.log(f"{self.__str__}:infer_edc_col_typ")
        self.set_edc_float_cols()
        self.set_edc_str_cols()
        kwargs = {"grpkey":self.edc_grpkey, "numcols":self._edc_col_type["num"], "strcols":self._edc_col_type["str"]}
        self.edc_data = SpcYx.merge_edc_data(self.edc_data_c1, kwargs)
        Logger.log(f"{self.__str__}:wrangle_edc_data merge_edc_data edc_data has row count: {self.edc_data.count} ")

    def fillna_edc_data(df:pd.DataFrame):
        edc_data_c2 = df.groupby(SpcYx.edc_grpkey).apply(lambda x: x.ffill().bfill())
        #edc_data_c2_temp = df.groupby(SpcYx.edc_grpkey).fillna(method='ffill').fillna(method='bfill')
        #edc_data_c2 = edc_data_c2_temp.fillna(method='ffill').fillna(method='bfill')
        return edc_data_c2

    def infer_edc_col_type(df:pd.DataFrame,rowkey=None):
        """The returning info has 3 types by dic 
        1. self._edc_col_type["all"] :all columns
        2. self._edc_col_type["num"] :numeric type columns
        3. self._edc_col_type["str"] :string type columns
        """
        types = PdExt.coltype(df,rowkey)
        Logger.log(f"infer_edc_col_type : {types} ")
        return types

    def set_edc_float_cols(self):
        if self._edc_col_type is None: self.infer_edc_col_type()
        # for ncol in self._edc_col_type["num"]:
        #    self.edc_data_c1[ncol].astype("float")
        self.edc_data_c1[self._edc_col_type["num"]].applymap(float)
        Logger.log(f"{self.__str__}:set_edc_float_cols")
 
    def set_edc_str_cols(self):
        if self._edc_col_type is None: self.infer_edc_col_type()
        self.edc_data_c1[self._edc_col_type["str"]].applymap(str)
        Logger.log(f"{self.__str__}:set_edc_str_cols")

    def merge_edc_data(df:pd.DataFrame, kwargs):
        """
        groupkey: used for groupby
        coltype: 1: num -> numeric types 2: str -> string types
        The merge approach is firstly seperate the edc data into 3 partions,
        partion 1 is the the group keys demonstrate the row key
        partion 2 is the numeric part and partion 3 is the non-numeric part.
        edc_data3 is thus partion 1 and the partion 2, edc_data4 is the partion 1 and the partion 3.
        the final edc_data5 is to merge by concating partion 1 and partion 2
        """
        grpkey = kwargs["grpkey"]
        numcols = kwargs["numcols"]
        strcols = kwargs["strcols"]
        edc_data3 = df.groupby(grpkey)[numcols].agg('mean')
        Logger.log(f"merge_edc_data:edc_data3")
        edc_data4 = df.groupby(grpkey)[strcols].agg('min')
        Logger.log(f"merge_edc_data:edc_data4")
        edc_data5 = pd.concat([edc_data3, edc_data4], axis=1)
        edc_data = edc_data5
        Logger.log(f"merge_edc_data:edc_data5")
        return edc_data

    def merge_spc_edc_data(self):
        """"merget the spc and edc by joining merging keys
            the merging key of spc : []
            the merging key of edc : []
        """
        self.spcyx_data = self.spc_data.merge(self.edc_data, how= "inner", left_on=self.spc_join_key, right_on=self.edc_join_key)
        
        Logger.log(f"{self.__str__}:merge_spc_edc_data:{self.spcyx_data}")

    def append_hdf5(self, appended):
        """save data objects into appended (path to hdf5 file)"""
        spcyx_data = self.spcyx_data
        spcyx_data.to_hdf(appended, key='spcyxdata')
        spc_data = self.spc_data
        spc_data.to_hdf(appended, key='spcdata')
        edc_data = self.edc_data
        edc_data.to_hdf(appended, key='edc_data')
        item_list = self.item_list
        item_list.to_hdf(appended, key='edcitems')
        eqpt_list = self.eqpt_list
        eqpt_list.to_hdf(appended, key='eqptlist')
        return appended

def get_spcyx_data(info,redis_key):
    """return status code has 
        200 Sucess proceeded the request with content
        204 Sucess proceeded the request without content 
        503 Service Unavailable"""
    try:
        redis = RedisDb.default()
        redis.set(redis_key,'start job',600)
        info = info
        spcyx = SpcYx(info, redis_key)
        spcyx.get_spc_data()
        if spcyx.spc_data.empty:
            return {"status":204,"message":"done","query info":info,"result":"empty spc data"}
        spcyx.get_item_list(restrict_op=False)
        if spcyx.item_list.empty:
            return {"status":204,"message":"done","query info":info,"result":"empty item_list data"}
        spcyx.get_eqpt_list()
        if spcyx.eqpt_list.empty:
            return {"status":204,"message":"done","query info":info,"result":"empty eqpt_list data"}
        spcyx.get_edc_data()
        if spcyx.edc_data_raw.empty:
            return {"status":204,"message":"done","query info":info,"result":"empty edc_data data"}
        spcyx.wrangle_edc_data()
        spcyx.merge_spc_edc_data()
        redis.set(redis_key,'data convert to csv file',600)
        csvfilename = f"{redis_key}.csv"
        csvfilepath = os.path.join("temp",csvfilename)
        spcyx.spcyx_data.to_csv(csvfilepath,index=False)

        hdf5filename = f"{redis_key}.hdf5"
        hdf5filepath = os.path.join("temp",hdf5filename)
        spcyx.append_hdf5(hdf5filepath)
        redis.set(redis_key,'done',60000)
        return {"status":200,"message":"done","csv file":[csvfilepath,csvfilename],"hdf5 file":[hdf5filepath,hdf5filename]}

    except Exception as e:
        redis.set(redis_key,'error',600)
        Logger.log(traceback.format_exc())