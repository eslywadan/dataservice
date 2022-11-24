import pandas as pd
import numpy as np
import os
from tools.config_loader import ConfigLoader

def get_fab_proc_csv():
    system_config = ConfigLoader.config("system")
    static_data_path = system_config["static_data_path"]
    return os.path.join(*static_data_path, 'edc_fab_proc.csv')

def get_fab_list():
    csv = get_fab_proc_csv()
    df = pd.read_csv(csv)
    ndarray = np.unique(df.FAB.values)
    fabs = ndarray.tolist()
    fabs.sort()
    return fabs

def get_proc_list(fab):
    csv = get_fab_proc_csv()
    df = pd.read_csv(csv)
    ndarray = df.PROC[df.FAB==fab].values
    procs = ndarray.tolist()
    procs.sort()
    return procs

