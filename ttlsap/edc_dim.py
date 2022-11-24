from dbtools.sql_buffer import SqlBuffer
from dbtools.query_db import query_list

def get_eqpt_list(fab, process, start, end, product='*', operation='*', recipe='*', owner_code='*'):
    sql = f'\n\tSELECT DISTINCT EQPT_ID \n\t  FROM PDATA_EDA.MEA_EDC_{fab}'

    buf = SqlBuffer(sql) \
        .add_like("EQPT_ID", process) \
        .add_date("TXN_DTTM", start, end) \
        .add("PROD_ID", product) \
        .add("OPRA_ID", operation) \
        .add("RECIPE_ID", recipe) \
        .check_owner_code(owner_code) \
        .order_by("EQPT_ID")

    return query_list(buf.sql)


def get_prod_list(fab, process, start, end, equipment='*', operation='*', owner_code='*'):
    sql = f'\n\tSELECT DISTINCT PROD_ID \n\t  FROM PDATA_EDA.MEA_EDC_{fab}'

    buf = SqlBuffer(sql) \
        .add_date("TXN_DTTM", start, end) \
        .add("EQPT_ID", equipment) \
        .add("OPRA_ID", operation) \
        .add_not_null("PROD_ID") \
        .check_owner_code(owner_code) \
        .order_by("PROD_ID")

    return query_list(buf.sql)


def get_opra_list(fab, process, start, end, equipment='*', product='*', owner_code='*'):
    sql = f'\n\tSELECT DISTINCT OPRA_ID \n\t  FROM PDATA_EDA.MEA_EDC_{fab}'

    buf = SqlBuffer(sql) \
        .add_date("TXN_DTTM", start, end) \
        .add("EQPT_ID", equipment) \
        .add("PROD_ID", product) \
        .add_not_null("OPRA_ID") \
        .check_owner_code(owner_code) \
        .order_by("OPRA_ID")

    return query_list(buf.sql)


def get_recipe_list(fab, process, start, end, equipment='*', owner_code='*'):
    sql = f'\n\tSELECT DISTINCT RECIPE_ID \n\t  FROM PDATA_EDA.MEA_EDC_{fab}'

    buf = SqlBuffer(sql) \
        .add_date("TXN_DTTM", start, end) \
        .add("EQPT_ID", equipment) \
        .add_not_null("RECIPE_ID") \
        .check_owner_code(owner_code) \
        .order_by("RECIPE_ID")

    return query_list(buf.sql)


def get_edc_item_list(fab, process, start, end, equipment='*', product='*', operation='*', recipe='*', owner_code='*', with_type_code=True):

    mn_start = start.replace('-', '')[0:6]
    mn_end = end.replace('-', '')[0:6]

    sql = '\n\tSELECT DISTINCT EDC_ITEM_NAME \n\t  FROM PEDAMART.DIM_KFM_EDC_ITEM'

    buf = SqlBuffer(sql) \
        .add("SITE", fab) \
        .add("EQPT_ID", equipment) \
        .add_between_str("TXN_MN", mn_start, mn_end) \
        .add("OPRA_ID", operation) \
        .order_by("EDC_ITEM_NAME")

    return query_list(buf.sql)
