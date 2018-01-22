import matplotlib.pyplot as plt
import matplotlib as mpl
from plotting import plot_field as plot, add_colorbar
from functools import partial
from cdo import Cdo
from preprocess import pre_proc_file
from forecast import ForecastCalculator

pina2012 = '../data/sic/sic_OImon_MPI-ESM-LR_pinatu2012_r%si1p1_201301-202212.nc'
decs4e2012 = '../data/sic/sic_OImon_MPI-ESM-LR_decs4e2012_r%si1p1_201301-202212.nc'
pina2014 = '../data/sic/sic_OImon_MPI-ESM-LR_pinatu2014_r%si1p1_201501-202412.nc'
decs4e2014 = '../data/sic/sic_OImon_MPI-ESM-LR_decs4e2014_r%si1p1_201501-202412.nc'

cdo = Cdo()

# set font size
font = {
    'family' : 'normal',
    'weight' : 'bold',
    'size'   : 20
}
mpl.rc('font', **font)

plot = partial(plot, projection='npstere', min_val=-10., max_val=10.)

for i in range(0, 1):

    fig, ax = plt.subplots(figsize=(16, 9))
    pre_proc = partial(pre_proc_file, runmean=4, seas=None)
    calculator = ForecastCalculator('sic', 2, 3, plot, pre_proc)

    
    calculator.pre_proc = partial(pre_proc, month=3)
    diff_2012, var_2012 = calculator.add_difference_subplot(pina2012, decs4e2012, i, 1)
    diff_2014, var_2014 = calculator.add_difference_subplot(pina2014, decs4e2014, i, 2)
    calculator.add_double_difference_subplot(diff_2012, var_2012, diff_2014, var_2014, i, 3)
    calculator.axes[1].set_ylabel('Sea Ice maximum (MAR)', labelpad=18, x=1.06)
    calculator.axes[1].set_title('Initialized 2012', y=1.06)
    calculator.axes[2].set_title('Initialized 2014', y=1.06)
    calculator.axes[3].set_title('2012 - 2014', y=1.03)
         
    calculator.pre_proc = partial(pre_proc, month=9)
    diff_2012, var_2012 = calculator.add_difference_subplot(pina2012, decs4e2012, i, 4)
    diff_2014, var_2014 = calculator.add_difference_subplot(pina2014, decs4e2014, i, 5)
    calculator.add_double_difference_subplot(diff_2012, var_2012, diff_2014, var_2014, i, 6)
    calculator.axes[4].set_ylabel('Sea Ice minimum (SEP)', labelpad=18)
    
    add_colorbar(fig, calculator.cs, label='Sea Ice Area Fraction Anomaly [%]')
    fig.tight_layout()
    plt.savefig('../plots/sic/4-yearly/%s-%s_minmax.png' % (i+1, i+4))

plt.show()
