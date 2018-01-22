import numpy as np
from scipy.io import netcdf


def open_file(fn, var_name):
    f = netcdf.netcdf_file(fn, 'r')
    return np.array(f.variables[var_name].data).squeeze()


def open_ensemble(path, variable, pre_proc=None):

    res = list()
    for i in range(1, 11):
        if pre_proc:
            fn = pre_proc(path % i)
        else:
            fn = path % i
        res.append(open_file(fn, variable))
    return np.ma.masked_equal(np.array(res), 1e20)

