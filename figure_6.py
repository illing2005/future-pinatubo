import matplotlib.pyplot as plt
import matplotlib as mpl
from plotting import plot_fldmean as plot, AxesFormatter
from functools import partial
from cdo import Cdo
from preprocess import pre_proc_fldmean
from forecast import ForecastCalculator

pina2012 = '../data/sic/sic_OImon_MPI-ESM-LR_pinatu2012_r%si1p1_201301-202212.nc'
decs4e2012 = '../data/sic/sic_OImon_MPI-ESM-LR_decs4e2012_r%si1p1_201301-202212.nc'
pina2014 = '../data/sic/sic_OImon_MPI-ESM-LR_pinatu2014_r%si1p1_201501-202412.nc'
decs4e2014 = '../data/sic/sic_OImon_MPI-ESM-LR_decs4e2014_r%si1p1_201501-202412.nc'

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

pre_proc_fldmean = partial(pre_proc_fldmean, runmean=4, selbox='30,90,70,85', month=3)
plot = partial(plot, y_range=[-10, 10], x_range=[-0.5, 6.5])
calculator = ForecastCalculator('sic', rows, cols, plot, pre_proc_fldmean, y_text=3.5)
formatter = AxesFormatter(
    range(0,7),
    range(-10, 11),
    'Leadtimes [yr]',
    'Sea Ice Area Fraction [%]',
    ['1-4', '2-5', '3-6', '4-7', '5-8', '6-9', '7-10']
)
calculator.formatter = formatter

fig, ax = plt.subplots(figsize=(12, 12))
formatter.show_legend = False


formatter.yticks = range(60, 80, 5)
calculator.plot = partial(plot, y_range=[60, 75])
calculator.y_text = 73.5
formatter.title = 'Initialized 2012\nNordic Sea (30$^\circ$E,90$^\circ$E,70$^\circ$N,85$^\circ$N) - SIC Maximum (MAR)'
calculator.add_difference_subplot_fldmean(pina2012, decs4e2012, 1)
formatter.title = 'Initialized 2014\nNordic Sea (30$^\circ$E,90$^\circ$E,70$^\circ$N,85$^\circ$N) - SIC Maximum (MAR)'
calculator.add_difference_subplot_fldmean(pina2014, decs4e2014, 2)

formatter.title = 'Bering Sea (165$^\circ$E,195$^\circ$E,55$^\circ$N,70$^\circ$N) - SIC Maximum (MAR)'
formatter.yticks = range(45, 80, 10)
calculator.y_text = 72
calculator.plot = partial(plot, y_range=[45, 75])
pre_proc_fldmean = partial(pre_proc_fldmean, selbox='165,195,55,70')
calculator.pre_proc = pre_proc_fldmean
calculator.add_difference_subplot_fldmean(pina2012, decs4e2012, 3)
calculator.add_difference_subplot_fldmean(pina2014, decs4e2014, 4)

formatter.title = 'Arctic (180$^\circ$W,180$^\circ$E,70$^\circ$N,90$^\circ$N - SIC Minimum (SEP))'
formatter.yticks = range(25, 50, 5)
calculator.y_text = 43
calculator.plot = partial(plot, y_range=[25, 45])
calculator.pre_proc = partial(pre_proc_fldmean, selbox='-180,180,70,90', month=9)
calculator.add_difference_subplot_fldmean(pina2012, decs4e2012, 5)
formatter.show_legend = True
calculator.add_difference_subplot_fldmean(pina2014, decs4e2014, 6)

fig.tight_layout()
plt.savefig('../plots/sic/4-yearly/fldmean_minmax.png')
plt.show()
