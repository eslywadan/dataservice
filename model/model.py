from pydantic import BaseModel
from typing import Optional


class auth_token(BaseModel):
    token: str


class login_token(BaseModel):
    CertificateKey: str


class chart_id_list(BaseModel):
    fab:str
    chart_list:str
    token:str
    start_dttm:str
    end_dttm:str
    method:str


class spc_data_info(chart_id_list):
    product:str
    pproc_id:str
    peqpt_id:str
    precipe_id:str
    owner_code:str
    run_mode:str
    spc_item_id:str
    proc_id:str
    delete_str_edc :Optional[str] = 'true'
    specify_edc_fab : Optional[str] = 'all'
    oos_filter :Optional[str] = 'false'
    specify_edc_eqpt : Optional[str] = 'all'
    data_type : Optional[str] = 'all'
    val_cols : Optional[str] = 'all'
    spc_chart_type_cd: Optional[str] = ""
    table_col: Optional[str] = ""
    oos_sql: Optional[str] = ""
    start_dttm_c1: Optional[str] = ""
    end_dttm_c1: Optional[str] = ""
    fab_pub: Optional[str] = ""