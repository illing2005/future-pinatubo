from scipy.io import netcdf
from scipy.stats import ttest_ind
import numpy as np
import numpy.ma as ma
from scipy.stats import t


def calc_ensemble_difference(ens1, ens2):

    i_max = ens1.shape[0]
    j_max = ens2.shape[0]
    diff_shape = (i_max*j_max,) + ens1.shape[1:]
    ind = 0
    result = np.zeros(diff_shape)
    for i in range(0, i_max):
        for j in range(0, j_max):
            result[ind, :] = ens1[i, :] - ens2[j, :]
            ind += 1
    return result

def calc_sig_of_difference(diff_1, diff_2, var_1, var_2):
    s_diff = estimate_s(var_1, var_2)
    test_value = t_value(diff_1, diff_2, s_diff)
    x = t.ppf(.95, 18)  # df = n+m-2=18
    diff_all = diff_1 - diff_2
    diff_masked = ma.masked_less(test_value, x)
    return (diff_all, diff_masked)


def calc_sig_zero(decs4e_array):
    pina_array = np.zeros(decs4e_array.shape)
    res = ttest_ind(decs4e_array, pina_array, axis=0)
    pvalue = ma.masked_invalid(ma.masked_greater(res.pvalue, 0.05))
    decs_mean = np.mean(decs4e_array, axis=0)
    #diff_masked = ma.masked_array(decs4e_mean, mask=pvalue.mask)
    return (decs_mean, pvalue.mask)


def calc_sig(decs4e_array, pina_array):
    res = ttest_ind(decs4e_array, pina_array, axis=0)
    pvalue = ma.masked_invalid(ma.masked_greater(res.pvalue, 0.05))
    decs_mean = np.mean(decs4e_array, axis=0)
    pina_mean = np.mean(pina_array, axis=0)
    decs_var = np.var(decs4e_array, axis=0)
    pina_var = np.var(pina_array, axis=0)
    diff = pina_mean - decs_mean
    diff_masked = ma.masked_array(diff, mask=pvalue.mask)
    return (diff, pvalue.mask, decs_var + pina_var)

def estimate_s(sx, sy, m=10., n=10.):
    return ((m-1) * sx + (n-1) * sy) / (m+n-2)

def t_value(mx, my, s, m=10., n=10.):
    return np.sqrt(n*m/(n+m)) * (np.abs(mx - my)) / np.sqrt(s)




