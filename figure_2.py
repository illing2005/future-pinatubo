# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
from plotting import plot_fldmean as plot, AxesFormatter
from functools import partial
from cdo import Cdo
from preprocess import pre_proc_file
from forecast import ForecastCalculator

decs4e2012_SUB = '../data/2012/tas_Amon_MPI-ESM-LR_decs4e2012_r%si1p1_201301-202212.nc'
pina2012_SUB = '../data/2012/tas_Amon_MPI-ESM-LR_pinatu2012_r%si1p1_201301-202212.nc'
decs4e2014_SUB = '../data/2014/tas_Amon_MPI-ESM-LR_decs4e2014_r%si1p1_201501-202412.nc'
pina2014_SUB = '../data/2014/tas_Amon_MPI-ESM-LR_pinatu2014_r%si1p1_201501-202412.nc'


rows = 4
cols = 2

cdo = Cdo()

# set font size
font = {
    'family' : 'normal',
    'weight' : 'normal',
    'size'   : 14
}
mpl.rc('font', **font)

season = None
x_val = range(0, 7)

pre_proc_fldmean = partial(pre_proc_file, seas=season, runmean=4, fldmean=True)
plot = partial(plot, x_range=[-.5, 7.5])

calculator = ForecastCalculator('tas', rows, cols, plot, pre_proc_fldmean)
formatter = AxesFormatter(
    range(0, 7),
    [287.4, 287.6, 287.8, 288.0, 288.2],
    'Leadtimes [yr]', 
    'Temperature [K]', 
    xticklabels=['1-4', '2-5', '3-6', '4-7', '5-8', '6-9', '7-10'],
    yticklabels=['287.4', '287.6', '287.8', '288.0', '288.2']
)

fig, ax = plt.subplots(figsize=(12, 16))

# global
formatter.title = 'Initialized 2012\nGlobal'
calculator.plot = partial(plot, y_range=[287.4, 288.2], x_range=[-.5, 6.5])
calculator.y_text = 288.1
calculator.formatter = formatter
calculator.add_difference_subplot_fldmean(pina2012_SUB, decs4e2012_SUB, 1)
formatter.show_legend = False
formatter.title = 'Initialized 2014\nGlobal'
calculator.add_difference_subplot_fldmean(pina2014_SUB, decs4e2014_SUB, 2)

# north atlantic
formatter.title = 'North Atlantic (60$^\circ$W,0$^\circ$W,50$^\circ$N,65$^\circ$N)'
formatter.yticklabels = ['279.2', '279.4', '279.6', '279.8', '280.0']
formatter.yticks = [279.2, 279.4, 279.6, 279.8, 280]
calculator.y_text = 279.9
calculator.plot = partial(plot, y_range=[279.2, 280.], x_range=[-.5, 6.5])
calculator.pre_proc = partial(pre_proc_fldmean, selbox='-60,0,50,65')
calculator.add_difference_subplot_fldmean(pina2012_SUB, decs4e2012_SUB, 3)
calculator.add_difference_subplot_fldmean(pina2014_SUB, decs4e2014_SUB, 4)   

# europe
formatter.title = 'Europe (10$^\circ$W,35$^\circ$E,30$^\circ$N,75$^\circ$N)'
formatter.yticklabels = ['284.5', '284.7', '284.9', '285.1', '285.3', '285.5']
formatter.yticks = [284.5, 284.7, 284.9, 285.1, 285.3, 285.5]
calculator.plot = partial(plot, y_range=[284.5, 285.5], x_range=[-.5, 6.5])
calculator.y_text = 285.4
calculator.pre_proc = partial(pre_proc_fldmean, selbox='-10,35,30,75')
calculator.add_difference_subplot_fldmean(pina2012_SUB, decs4e2012_SUB, 5)
calculator.add_difference_subplot_fldmean(pina2014_SUB, decs4e2014_SUB, 6)


formatter.title = 'North Pacific Basin (130$^\circ$E,250$^\circ$E,20$^\circ$N,60$^\circ$N)'
formatter.yticklabels = ['287.5', '287.7', '287.9', '288.1', '288.3', '288.5,']
formatter.yticks = [287.5, 287.7, 287.9, 288.1, 288.3, 288.5]
calculator.plot = partial(plot, y_range=[287.5, 288.5], x_range=[-.5, 6.5])
calculator.y_text = 288.4
calculator.pre_proc = partial(pre_proc_fldmean, selbox='130,250,20,60', seamask_fine=True)
calculator.add_difference_subplot_fldmean(pina2012_SUB, decs4e2012_SUB, 7)
formatter.show_legend = True
calculator.add_difference_subplot_fldmean(pina2014_SUB, decs4e2014_SUB, 8)

fig.tight_layout()

plt.savefig('../plots/tas/4-yearly/fldmean_4-yearly_labeled.png')

plt.show()

