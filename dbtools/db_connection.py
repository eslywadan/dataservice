import os
import sqlite3
import psycopg2 as pg
from tools.config_loader import ConfigLoader
from tools.sec_loader import SecretLoader
from tools.logger import Logger
import phoenixdb

class DbConnection:
    _db_list = []
    _default_db_id = 0
    _account_db_id = 4

    #取得預設的DB連線
    @classmethod
    def default(clz):
        clz.check_db_config()
        return clz.connection(clz._default_db_id)

    #取得預設的account DB連線
    @classmethod
    def account_db(clz):
        clz.check_db_config()
        return clz.connection(clz._account_db_id)

    #取得預設的cdp hbase連線
    @classmethod
    def cdp_hbase(clz):
        clz.check_db_config()
        cred = SecretLoader.secret("cdp_hbase")
        return clz.connection(clz._cdp_hbase_id,cred)

    #取得預設的cdp phoenix連線
    @classmethod
    def cdp_phoenix(clz):
        clz.check_db_config()
        return clz.connection(clz._cdp_phoenix_id)


    #取得預設的edw gp連線
    @classmethod
    def edw_gp(clz):
        clz.check_db_config()
        cred = SecretLoader.secret("edw_gp")
        return clz.connection(clz._edw_gp_id,cred)


    #以DB id，產生DB connection instance
    @classmethod
    def connection(clz, db_id,cred={}):
        clz.check_db_config()
        db_info = clz._db_list[db_id]
        func_name = f'get_{db_info["type"]}_connection'
        func = getattr(clz, func_name)
        connection = func(db_info["connection_string"], db_info["driver_path"],cred)
        return connection


    @classmethod
    def check_db_config(clz):
        if len(clz._db_list) == 0:
            db_config = ConfigLoader.config("database")
            clz._db_list = db_config["database_list"]
            clz._default_db_id = db_config["default"]
            clz._account_db_id = db_config["account_db"]
            clz._cdp_hbase_id = db_config["cdp_hbase"]
            clz._edw_gp_id = db_config["edw_gp"]
            clz._cdp_phoenix_id = db_config["cdp_phoenix"]


    @classmethod
    def reset_db_config(clz):
        clz._db_list = []
        clz._default_db_id = 0


    #以connection string, driver path，直接產生DB connection instance
    @staticmethod
    def get_phoenix_connection(connection_string, driver_path=None, cred=None):
        return phoenixdb.connect(connection_string)

    @staticmethod
    def get_phoenixdb_connection(connection_string, driver_path=None, cred=None):
        return phoenixdb.connect(connection_string)

    @staticmethod
    def get_greenplum_connection(connection_string, driver_path,cred=None):
        Logger.log(f"open gp db conn {connection_string}")
        dbname = connection_string["dbname"]
        host = connection_string["host"]
        port = connection_string["port"]
        user = cred["usr"]
        password = cred["pass"]
        conn = pg.connect(dbname=dbname,host=host, port=port, user=user, password=password)
        return conn

    @staticmethod
    def get_sqlite_connection(connection_string, driver_path,cred=None):
        return sqlite3.connect(connection_string)

