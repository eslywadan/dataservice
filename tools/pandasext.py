import pandas as pd

class PdExt():

  def coltype(df:pd.DataFrame,rowkey=None):
    """"
    Return by {"all":full_col_index,"num":num_col_index,"str":str_col_index}
    """
    full_col_series = df.count()
    full_col_index = full_col_series.index
    full_col_index = full_col_index.difference(rowkey)
    num_col_series = df.mean()
    num_col_index = num_col_series.index
    str_col_index = full_col_index.difference(num_col_index)
    return {"all":full_col_index,"num":num_col_index,"str":str_col_index}
    
