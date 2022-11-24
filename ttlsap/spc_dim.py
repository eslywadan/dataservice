from dbtools.sql_buffer import SqlBuffer
from dbtools.query_db import query_list

def get_spc_opra_list(fab, process='*', start='', end='', equipment='*', owner_code='*'):

    mn_start = start.replace('-', '')[0:6]
    mn_end = end.replace('-', '')[0:6]

    sql = '\n\tSELECT DISTINCT OPRA_ID \n\t  FROM PEDAMART.DIM_KFM_SPC_ITEM'

    buf = SqlBuffer(sql) \
        .add("SITE", fab) \
        .add_between_str("PRODN_MN", mn_start, mn_end) \
        .add_not_null("OPRA_ID") \
        .order_by("OPRA_ID")

    return query_list(buf.sql)


def get_spc_item_list(fab, process='*', start='', end='', equipment='*', owner_code='*'):

    mn_start = start.replace('-', '')[0:6]
    mn_end = end.replace('-', '')[0:6]

    sql = '\n\tSELECT DISTINCT SPC_ITEM_ID \n\t  FROM PEDAMART.DIM_KFM_SPC_ITEM'

    buf = SqlBuffer(sql) \
        .add("SITE", fab) \
        .add_between_str("PRODN_MN", mn_start, mn_end) \
        .add_not_null("SPC_ITEM_ID") \
        .order_by("SPC_ITEM_ID")

    return query_list(buf.sql)
