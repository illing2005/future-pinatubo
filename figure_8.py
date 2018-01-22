import numpy as np
from scipy.io import netcdf
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import numpy.ma as ma
from scipy.stats import t
from plotting import plot_fldmean as plot, AxesFormatter
from significance import calc_sig, t_value, estimate_s, calc_sig_of_difference
from ensemble_io import open_ensemble
from functools import partial
from cdo import Cdo
from preprocess import pre_proc_file, pre_proc_fldmean
from forecast import ForecastCalculator

pina2012 = '../data/pr/pr_Amon_MPI-ESM-LR_pinatu2012_r%si1p1_201301-202212.nc'
decs4e2012 = '../data/pr/pr_Amon_MPI-ESM-LR_decs4e2012_r%si1p1_201301-202212.nc'
pina2014 = '../data/pr/pr_Amon_MPI-ESM-LR_pinatu2014_r%si1p1_201501-202412.nc'
decs4e2014 = '../data/pr/pr_Amon_MPI-ESM-LR_decs4e2014_r%si1p1_201501-202412.nc'

rows = 3
cols = 2

cdo = Cdo()

# set font size
font = {
    'family' : 'normal',
    'weight' : 'normal',
    'size'   : 14
}
mpl.rc('font', **font)

pre_proc_fldmean = partial(pre_proc_fldmean, runmean=4, multiplier=86400)
plot = partial(plot, y_range=[-0.05, .05], x_range=[-0.5, 6.5])
calculator = ForecastCalculator('pr', rows, cols, plot, pre_proc_fldmean, y_text=0.04)
formatter = AxesFormatter(
    range(0, 7),
    [2.90, 2.92, 2.94, 2.96, 2.98],
    'Leadtimes [yr]',
    'Precipitation [mm day$^{-1}$]',
    #range(1, 11),
    ['1-4', '2-5', '3-6', '4-7', '5-8', '6-9', '7-10']
)
calculator.formatter = formatter

fig, ax = plt.subplots(figsize=(12, 12))

formatter.title = 'Initialized 2012\nGlobal'
calculator.plot = partial(plot, y_range=[2.90, 2.98])
calculator.y_text = 2.97
calculator.add_difference_subplot_fldmean(pina2012, decs4e2012, 1)
formatter.title = 'Initialized 2014\nGlobal'
formatter.show_legend = False
calculator.add_difference_subplot_fldmean(pina2014, decs4e2014, 2)

formatter.title = 'Ocean Precipitation'
calculator.plot = partial(plot, y_range=[2.92, 3.00])
formatter.yticks = [2.92, 2.94, 2.96, 2.98, 3.00]
calculator.y_text = 2.99
calculator.pre_proc = partial(pre_proc_fldmean, seamask=True)
calculator.add_difference_subplot_fldmean(pina2012, decs4e2012, 3)
calculator.add_difference_subplot_fldmean(pina2014, decs4e2014, 4)

formatter.title = 'Land precipitation'
calculator.pre_proc = partial(pre_proc_fldmean, landmask=True)
calculator.plot = partial(plot, y_range=[2.96, 3.06])
formatter.yticks = [2.96, 2.98, 3.0, 3.02, 3.04, 3.06]
calculator.y_text = 3.05
calculator.add_difference_subplot_fldmean(pina2012, decs4e2012, 5)
calculator.add_difference_subplot_fldmean(pina2014, decs4e2014, 6)

fig.tight_layout()
plt.savefig('../plots/pr/4-yearly/fldmean_ocean_land_full.png')
plt.show()
