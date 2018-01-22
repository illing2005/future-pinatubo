from matplotlib import pyplot as plt
from functools import partial
from cdo import Cdo
import matplotlib

from plotting import plot_field as plot, add_colorbar
from preprocess import pre_proc_file
from forecast import ForecastCalculator

decs4e2012_SUB = '../data/tas_Amon_MPI-ESM-LR_decs4e2012_r%si1p1_201301-202212.nc'
pina2012_SUB = '../data/tas_Amon_MPI-ESM-LR_pinatu2012_r%si1p1_201301-202212.nc'
decs4e2014_SUB = '../data/2014/tas_Amon_MPI-ESM-LR_decs4e2014_r%si1p1_201501-202412.nc'
pina2014_SUB = '../data/2014/tas_Amon_MPI-ESM-LR_pinatu2014_r%si1p1_201501-202412.nc'

cdo = Cdo()

rows = 3
cols = 2

pre_proc_season = partial(pre_proc_file, seas=None, runmean=4, selbox='-250,110,-90,90')
fig, ax = plt.subplots(figsize=(16, 14))

calculator = ForecastCalculator('tas', 3, 2, plot, pre_proc_season)

# set font size
font = {
    'family' : 'normal',
    'weight' : 'bold',
    'size'   : 20
}
matplotlib.rc('font', **font)
   
# leadtime 1-4 (right column)
diff_2012, var_2012 = calculator.add_difference_subplot(pina2012_SUB, decs4e2012_SUB, 0, 1)
diff_2014, var_2014 = calculator.add_difference_subplot(pina2014_SUB, decs4e2014_SUB, 0, 3)
calculator.add_double_difference_subplot(diff_2012, var_2012, diff_2014, var_2014, 0, 5)

# leadtime 7-10 (right column)
diff_2012, var_2012 = calculator.add_difference_subplot(pina2012_SUB, decs4e2012_SUB, 6, 2)
diff_2014, var_2014 = calculator.add_difference_subplot(pina2014_SUB, decs4e2014_SUB, 6, 4)
calculator.add_double_difference_subplot(diff_2012, var_2012, diff_2014, var_2014, 6, 6)

add_colorbar(fig, calculator.cs, label='Temperature Anomaly [K]')
calculator.axes[1].set_title('Leadyear 1-4', y=1.03)
calculator.axes[2].set_title('Leadyear 7-10', y=1.03)
calculator.axes[1].set_ylabel('Initialized 2012')
calculator.axes[3].set_ylabel('Initialized 2014')
calculator.axes[5].set_ylabel('2012 - 2014')

plt.savefig('/../plots/tas/4-yearly/LY_1-4_and_7-10_maps.png')

plt.show()

