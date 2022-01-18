from dbtools.sql_buffer import SqlBuffer, get_measure_column, get_item_columns
from dbtools.query_db import query_table, join_dict

def get_edc_data(fab, process, start, end, equipment, 
    product='*', operation='*', recipe='*', 
    owner_code='*', chamber_code='00', 
    build_sql_only=False, data_shape_wide=True, prfx_opra_eqpt=False, 
    edc_items=[]):
    item_select, item_column = get_item_columns(operation, equipment, edc_items, prfx_opra_eqpt)

    sql = f'''
    SELECT GLS_ID, OPRA_ID, PROD_ID, EQPT_ID, RECIPE_ID, 
           TO_CHAR(CONVERT_TZ(TXN_DTTM, 'UTC', 'Asia/Taipei'), 'yyyy-MM-dd HH:mm:ss') AS TXN_DTTM{item_select}
      FROM PDATA_EDA.MEA_EDC_{fab}{item_column}'''

    buf = SqlBuffer(sql) \
        .add_date("TXN_DTTM", start, end) \
        .add("EQPT_ID", equipment) \
        .add("PROD_ID", product) \
        .add("OPRA_ID", operation) \
        .add("RECIPE_ID", recipe) \
        .check_owner_code(owner_code) \
        .check_chamber_code(chamber_code) \
        .order_by(6)

    return query_table(buf.sql)


def get_spc_data(fab, process='*', start='', end='', equipment='*', 
    spc_operation='*', 
    owner_code='*', measure_type=0, 
    build_sql_only=False, data_shape_wide=True, 
    spc_items=[],
    edc_pnl=False, spc_pnl=False):

    sql = f'''
    SELECT DISTINCT {'PNL_ID AS GLS_ID' if edc_pnl else 'GLS_ID'}, 
           TO_CHAR(CONVERT_TZ(DATA_DTTM, 'UTC', 'Asia/Taipei'), 'yyyy-MM-dd HH:mm:ss') AS DTTM, SPC_ITEM_ID, 
           {get_measure_column(measure_type)} AS MEAS_VAL
      FROM PDATA_EDA.MEA_SPC_{fab}_PARA'''

    line_eqpt = equipment[0:6] if len(equipment) >= 6 else equipment

    buf = SqlBuffer(sql) \
        .add_date("DATA_DTTM", start, end) \
        .add("OPRA_ID", spc_operation) \
        .add_like("PV_EQUIP_ID", line_eqpt) \
        .check_owner_code(owner_code) \
        .add_in("SPC_ITEM_ID", spc_items) \
        .order_by("DTTM")

    if data_shape_wide:
        return query_table(buf.sql, 'GLS_ID', 'SPC_ITEM_ID', 'MEAS_VAL', merge_pnl=not edc_pnl and spc_pnl)
    else:        
        return query_table(buf.sql)

def is_panel(fab, operation):
    return len(fab) == 2 and fab[0].upper()=='L' and len(operation) >= 4 and operation[0:4].isnumeric() and int(operation[0:4]) >= 3000 \
        or len(fab) == 4 and fab[2].upper()=='L' and len(operation) >= 4 and operation[0:4].isnumeric() and int(operation[0:4]) >= 6500

def get_edc_spc_data(fab, process='*', start='', end='', spc_end='', equipment='*', 
    product='*', operation='*', recipe='*', spc_operation='*', 
    owner_code='*', chamber_code='00', measure_type=0, 
    build_sql_only=False, data_shape_wide=True, prfx_opra_eqpt=False, 
    edc_items=[], spc_items=[]):

    edc_pnl = is_panel(fab, operation)
    spc_pnl = is_panel(fab, spc_operation)

    spc_dict = get_spc_data(fab, process, start, spc_end, equipment, spc_operation, 
        owner_code, measure_type, build_sql_only, data_shape_wide, spc_items, edc_pnl, spc_pnl)

    line_eqpt = equipment[0:6] if len(equipment) >= 6 else equipment

        
    #ch200519:只有當edc已經是panel時，才以spc的PNL_ID找panel(edc的欄位名稱還是GLS_ID)
    spc_sql = f'''
    SELECT {'PNL_ID' if edc_pnl else 'GLS_ID'} 
      FROM PDATA_EDA.MEA_SPC_{fab}_PARA'''

    spc_buf = SqlBuffer(spc_sql) \
        .add_date("DATA_DTTM", start, spc_end) \
        .add("OPRA_ID", spc_operation) \
        .add_like("PV_EQUIP_ID", line_eqpt) \
        .check_owner_code(owner_code) \
        .add_in("SPC_ITEM_ID", spc_items)
    

    item_select, item_column = get_item_columns(operation, equipment, edc_items, prfx_opra_eqpt)

    sql = f'''
    SELECT GLS_ID, OPRA_ID, PROD_ID, EQPT_ID, RECIPE_ID, 
           TO_CHAR(CONVERT_TZ(TXN_DTTM, 'UTC', 'Asia/Taipei'), 'yyyy-MM-dd HH:mm:ss') AS TXN_DTTM{item_select}
      FROM PDATA_EDA.MEA_EDC_{fab}{item_column}'''

    buf = SqlBuffer(sql) \
        .add_date("TXN_DTTM", start, end) \
        .add("EQPT_ID", equipment) \
        .add("PROD_ID", product) \
        .add("OPRA_ID", operation) \
        .add("RECIPE_ID", recipe) \
        .check_owner_code(owner_code) \
        .check_chamber_code(chamber_code) \
        .add_in_sub("GLS_ID", spc_buf.sql)

    edc_dict = query_table(buf.sql)

    return join_dict(spc_dict, edc_dict, on='GLS_ID', sort='TXN_DTTM')
