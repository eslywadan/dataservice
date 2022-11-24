import pandas as pd
import numpy as np
from datetime import datetime
from dbtools.db_connection import DbConnection
from tools.logger import Logger

def query_list(sql):
    logger = Logger.default()
    logger.info(sql)

    t1 = datetime.now()
    #cn = get_phoenix_connection()
    cn = DbConnection.default()
    t2 = datetime.now()
    logger.info(f"Seconds for connecting: {(t2 - t1).total_seconds():.3f}")

    t3 = datetime.now()
    df = pd.read_sql_query(sql, cn)
    t4 = datetime.now()
    logger.info(f"Seconds for query: {(t4 - t3).total_seconds():.3f}")
    cn.close()

    first_col = df.columns.values[0]
    ndarray = df[first_col].values
    #ndarray = df.iloc[:, 0].values
    logger.info(f"Records found: {len(ndarray)}")

    return ndarray.tolist()


def query_table(sql, pivot_index=None, pivot_columns=None, pivot_values=None, merge_pnl=False):
    logger = Logger.default()
    logger.info(sql)

    t1 = datetime.now()
    #cn = get_phoenix_connection()
    cn = DbConnection.default()
    t2 = datetime.now()
    logger.info(f"Seconds for connecting: {(t2 - t1).total_seconds():.3f}")

    t3 = datetime.now()
    df = pd.read_sql_query(sql, cn)
    t4 = datetime.now()
    logger.info(f"Seconds for query: {(t4 - t3).total_seconds():.3f}")
    cn.close()
    
    logger.info(f"Records found: {len(df.index)}")

    if pivot_index:
        #ch200519:如果多個panel屬於同一片玻璃，以玻璃為單位作pivot，多個panel的數據要平均
        #           此外，如果同一片玻璃有多個數據，取最後一個
        aggfunc = np.mean if merge_pnl else get_last_one
        df = df.pivot_table(index=pivot_index, columns=pivot_columns, values=pivot_values, aggfunc=aggfunc).reset_index()
        logger.info(f"Pivoted records: {len(df.index)}")

    df = df.where(pd.notnull(df), None)
    return df.to_dict('records')


def join_dict(left_dict, right_dict, on=None, left_on=None, right_on=None, how='inner', sort=None):
    if len(left_dict) == 0 or len(right_dict) == 0: return []

    left_df = pd.DataFrame.from_dict(left_dict)
    right_df = pd.DataFrame.from_dict(right_dict)
    df = left_df.merge(right_df, on=on, left_on=left_on, right_on=right_on, how=how)
    if sort: df = df.sort_values(by=sort)

    #c200427:must replace NaN to None again
    df = df.where(pd.notnull(df), None)
    return df.to_dict('records')


def get_last_one(duplicated):
    return duplicated if len(duplicated) == 1 else duplicated[duplicated.index[-1]]

