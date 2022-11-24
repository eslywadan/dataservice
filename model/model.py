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

