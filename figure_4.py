
import matplotlib.pyplot as plt
from plotting import plot_vertical as plot, add_colorbar, add_number
from cdo import *
from ensemble_io import open_ensemble
from significance import calc_sig, calc_sig_of_difference
from preprocess import pre_proc_file
from functools import partial
cdo = Cdo()

decs4e2012 = '../data/ta/data/ta_Amon_MPI-ESM-LR_decs4e2012_r%si1p1_201301-202212.nc_ZONMEAN'
pina2012 = '../data/ta/data/ta_Amon_MPI-ESM-LR_pinatu2012_r%si1p1_201301-202212.nc_ZONMEAN'
decs4e2014 = '../data/ta/data/ta_Amon_MPI-ESM-LR_decs4e2014_r%si1p1_201501-202412.nc_ZONMEAN'
pina2014 = '../data/ta/data/ta_Amon_MPI-ESM-LR_pinatu2014_r%si1p1_201501-202412.nc_ZONMEAN'

rows = 1
cols = 3
timestep = 1

pre_process = partial(pre_proc_file, zonmean=True, runmean=4, remap=False)


for timestep in range(0,1):
    fig, ax = plt.subplots(figsize=(17, 4))
    pina2012_array = open_ensemble(pina2012, 'ta', pre_process)
    decs4e2012_array = open_ensemble(decs4e2012, 'ta', pre_process)
    diff_2012, sig_mask, var_2012 = calc_sig(decs4e2012_array, pina2012_array)
    ax = plt.subplot(rows, cols, 1)
    plot(ax, diff_2012[timestep,:,:])
    add_number(ax, 1, x=0, y=7, size=12)
    ax.set_title('Initialized 2012')
    ax.set_xticks([0, 48, 95])
    ax.set_xticklabels([-90, 0, 90])
    
    pina2014_array = open_ensemble(pina2014, 'ta', pre_process)
    decs4e2014_array = open_ensemble(decs4e2014, 'ta', pre_process)
    diff_2014, sig_mask, var_2014 = calc_sig(decs4e2014_array, pina2014_array)
    ax = plt.subplot(rows, cols, 2)
    plot(ax, diff_2014[timestep,:,:])
    add_number(ax, 2, x=0, y=7, size=12)
    ax.set_title('Initialized 2014')
    ax.set_xticks([0, 48, 95])
    ax.set_xticklabels([-90, 0, 90])

    diff_all, diff_masked = calc_sig_of_difference(diff_2012, diff_2014, var_2012, var_2014)
    ax = plt.subplot(1, 3, 3)
    add_number(ax, 3, x=0, y=7, size=12)
    cs = plot(ax, diff_all[timestep, :, :])

    ax.set_title('2012 - 2014')
    ax.set_xticks([0, 48, 95])
    ax.set_xticklabels([-90, 0, 90])

    add_colorbar(fig, cs, label='Temperature Anomaly [K]')
    plt.savefig('../plots/ta/4-yearly/%02d-%02d.png' % (timestep+1,timestep+4))

plt.show()
