from dbtools.db_connection import DbConnection
import tools.crypto as crypto
import pandas as pd
from dbtools.sql_buffer import SqlBuffer
from tools.redis_db import RedisDb
from datetime import datetime

def check_client_id_password(client_id, password):
    sql = '''
    SELECT CLIENT_ID, PASSWORD, TYPE, EXPIRY, PERMISSION 
      FROM ACCOUNT'''
    buf = SqlBuffer(sql).add("CLIENT_ID", client_id)
    cn = DbConnection.account_db()
    df = pd.read_sql_query(buf.sql, cn)
    if len(df.index) > 0:
        password_correct = df["PASSWORD"].values[0]
        type = df["TYPE"].values[0]        
        expiry = df["EXPIRY"].values[0]        
        permission = df["PERMISSION"].values[0]
        
        check_ok = (password_correct == crypto.crypto_password(type, password))

        if check_ok:
            today = datetime.today().strftime("%Y-%m-%d")
            check_ok = expiry > today

        if check_ok:
            token = crypto.get_account_token(client_id)
            redis = RedisDb.default()
            redis.set(token, f"{client_id}:{permission}", expiry_hours=24)
            return token


    return None
