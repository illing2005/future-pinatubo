import numpy as np
from scipy.io import netcdf
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import numpy.ma as ma
from scipy.stats import t
from plotting import plot_field as plot, add_colorbar
from significance import calc_sig, t_value, estimate_s, calc_sig_of_difference
from ensemble_io import open_ensemble
from functools import partial
from cdo import Cdo
from preprocess import pre_proc_file
from forecast import ForecastCalculator

pina2012 = '../data/climdex/fdetccdi/fdetccdi_yr_mpi-esm-lr_pinatu2012_r%si1p1_2013-2022.nc'
pina2014 = '../data/climdex/fdetccdi/fdetccdi_yr_mpi-esm-lr_pinatu2014_r%si1p1_2015-2024.nc'
decs4e2012 = '../data/climdex/fdetccdi/fdetccdi_yr_mpi-esm-lr_decs4e2012_r%si1p1_2013-2022.nc'
decs4e2014 = '../data/climdex/fdetccdi/fdetccdi_yr_mpi-esm-lr_decs4e2014_r%si1p1_2015-2024.nc'

cdo = Cdo()

# set font size
font = {
    'family' : 'normal',
    'weight' : 'bold',
    'size'   : 20
}
mpl.rc('font', **font)

plot = partial(plot, min_val=-10., max_val=10.)

for i in range(0, 1):

    fig, ax = plt.subplots(figsize=(16, 9))
    pre_proc = partial(pre_proc_file, runmean=4, seas=None, selbox='-250,110,-90,90')
    calculator = ForecastCalculator('fdetccdi', 1, 3, plot, pre_proc)

    diff_2012, var_2012 = calculator.add_difference_subplot(pina2012, decs4e2012, i, 1)
    diff_2014, var_2014 = calculator.add_difference_subplot(pina2014, decs4e2014, i, 2)
    calculator.add_double_difference_subplot(diff_2012, var_2012, diff_2014, var_2014, i, 3)

    add_colorbar(fig, calculator.cs, label='Frost day anomaly per year')

    calculator.axes[1].set_title('Initialized 2012', y=1.03)
    calculator.axes[2].set_title('Initialized 2014', y=1.03)
    calculator.axes[3].set_title('2012 - 2014', y=1.03)

    fig.tight_layout()
    plt.savefig('../plots/fdetccdi/4-yearly/ly%s-%s.png' % (i+1, i+4))

plt.show()
