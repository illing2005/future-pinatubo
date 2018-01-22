# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
from plotting import add_colorbar, plot_field as plot
from functools import partial
from cdo import Cdo
from preprocess import pre_proc_file
from forecast import ForecastCalculator

pina2012 = '../data/pr/2012/pr_Amon_MPI-ESM-LR_pinatu2012_r%si1p1_201301-202212.nc'
decs4e2012 = '../data/pr/2012/pr_Amon_MPI-ESM-LR_decs4e2012_r%si1p1_201301-202212.nc'
pina2014 = '../data/pr/2014/pr_Amon_MPI-ESM-LR_pinatu2014_r%si1p1_201501-202412.nc'
decs4e2014 = '../data/pr/2014/pr_Amon_MPI-ESM-LR_decs4e2014_r%si1p1_201501-202412.nc'

decs4e_array = []
pina_array = []

cdo = Cdo()

rows = 2
cols = 2

# set font size
font = {
    'family' : 'normal',
    'weight' : 'bold',
    'size'   : 20
}
mpl.rc('font', **font)

for timestep in range(0, 1):

    pre_proc_season = partial(pre_proc_file, runmean=4, selbox='-250,110,-90,90', multiplier=86400)

    fig, ax = plt.subplots(figsize=(16, 9))

    plot = partial(plot, min_val=-0.5, max_val=0.5, cmap=plt.cm.BrBG)

    calculator = ForecastCalculator('pr', 1, 3, plot, pre_proc_season)

    diff_2012, var_2012 = calculator.add_difference_subplot(pina2012, decs4e2012, timestep, 1)
    diff_2014, var_2014 = calculator.add_difference_subplot(pina2014, decs4e2014, timestep, 2)
    calculator.add_double_difference_subplot(diff_2012, var_2012, diff_2014, var_2014, timestep, 3)    

    calculator.axes[1].set_title('Initialized 2012', y=1.03)
    calculator.axes[2].set_title('Initialized 2014', y=1.03)
    calculator.axes[3].set_title('2012 - 2014', y=1.03)

    add_colorbar(fig, calculator.cs, label='Precipitation anomaly [mm day$^{-1}$]')

    plt.savefig('../plots/pr/4-yearly/year_%02d-%02d.png' % (timestep+1,timestep+4))

plt.show()

