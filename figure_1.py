import matplotlib as mpl
import numpy as np
from scipy.io import netcdf
from datetime import datetime, timedelta
from matplotlib import pyplot as plt


fig = plt.figure()

def aod(fig_id):

    fn = 'data/pinatubo_aod.nc'
    f = netcdf.netcdf_file(fn, 'r')
    aod = np.array(f.variables['AOD'].data).squeeze()
    lat = np.array(f.variables['lat'].data).squeeze()
    time = np.array(f.variables['time'].data).squeeze()
    cal_start = datetime.strptime('2000-01-01', '%Y-%m-%d')
    timelabels = []
    for val in time:
        tmp_date = cal_start + timedelta(days=val)
        timelabels.append(datetime.strftime(tmp_date, '%d-%m-%y'))

    colorSteps = [0., 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    norm = mpl.colors.BoundaryNorm(colorSteps, plt.cm.YlOrBr.N)
    ax = plt.subplot(*fig_id)
    cs = ax.contourf(time, lat, np.swapaxes(aod, 0, 1), levels=colorSteps, cmap=plt.cm.YlOrBr, norm=norm)
    ax.set_xticks([time[12], time[24], time[36]])
    ax.set_xticklabels(['Year 1', 'Year 2', 'Year 3'])
    ax.set_yticks(np.linspace(-80, 80, 9))
    ax.set_ylabel('Latitude')
    ax.axvline(time[16] + 2, color='black', linestyle='--')
    ax.axis([4779.98958333, 5690.98958333, -85, 85])
    ax.set_xlabel('Simulation time')
    cbar = plt.colorbar(cs, ax=ax, orientation="vertical")#, ticks=colorSteps[::2])
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('Simulated AOD', rotation=270)
    ax.set_title('AOD')
    ax.text(time[16] - 35, 12., 'Eruption in June', rotation=90)


def nao_assim(fig_id):

    fn ='data/nao_assim.nc'
    f = netcdf.netcdf_file(fn, 'r')
    ax = plt.subplot(*fig_id)
    nao = -1 * np.array(f.variables['pca_princ'].data).squeeze()[:, 0]
    time = np.array(f.variables['time'].data).squeeze()
    nao_plus = np.ma.masked_less(nao, 0)
    nao_minus = np.ma.masked_greater(nao, 0)
    cal_start = datetime.strptime('1960-01-01', '%Y-%m-%d')
    timelabels = []
    for val in time:
        tmp_date = cal_start + timedelta(days=val)
        timelabels.append(datetime.strftime(tmp_date, '%Y'))
    timelabels.append('2015')
    x = range(0, len(nao))
    ax.bar(x[:13], nao_plus[:13], align='center', width=1., color='red')
    ax.bar(x[:13], nao_minus[:13], align='center', width=1., color='blue')
    ax.bar(np.add(x[13:16], -0.25), nao_plus[13:16], align='center', width=.5, color='red')
    ax.bar(np.add(x[13:16], -0.25), nao_minus[13:16], align='center', width=.5, color='blue')
    ax.bar(x[16:35], nao_plus[16:35], align='center', width=1., color='red')
    ax.bar(x[16:35], nao_minus[16:35], align='center', width=1., color='blue')
    
    ax.bar(x[35:37], nao_plus[35:37], align='center', width=1., color='red')
    ax.bar(x[35:37], nao_minus[35:37], align='center', width=1., color='blue')
    ax.bar(np.add(x[37:40], -0.25), nao_plus[37:40], align='center', width=.5, color='red')
    ax.bar(np.add(x[37:40], -0.25), nao_minus[37:40], align='center', width=.5, color='blue')
    ax.bar(x[40:48], nao_plus[40:48], align='center', width=1., color='red')
    ax.bar(x[40:48], nao_minus[40:48], align='center', width=1., color='blue')

    ax.set_xticks([0, 12, 24, 36])
    ax.set_xticklabels(timelabels[::12]+['2015'])
    ax.axis([-0.5, len(x) - .5, -27500, 27500])
    ax.axvline(x[10], color='black')
    ax.axvline(x[34], color='black')
    ax.set_title('NAO')
    ax.set_xlabel('Time')
    cal_start = datetime.strptime('1961-01-01', '%Y-%m-%d')

    fn = 'data/nao_forecast.nc'
    f = netcdf.netcdf_file(fn, 'r')
    nao = np.array(f.variables['pca_princ'].data).squeeze()[:, 0]
    nao *= -1
    time = np.array(f.variables['time'].data).squeeze()
    timelabels = []
    for val in time:
        tmp_date = cal_start + timedelta(days=val)
        timelabels.append(datetime.strftime(tmp_date, '%%Y'))
    nao_plus = np.ma.masked_less(nao, 0)
    nao_minus = np.ma.masked_greater(nao, 0)
    x = range(0, len(nao))
    ax.bar(np.add(x[13:16], 0.25), nao_plus[13:16], align='center', width=.5, color='red', hatch="//", alpha=0.5)
    ax.bar(np.add(x[13:16], 0.25), nao_minus[13:16], align='center', width=.5, color='blue', hatch="//", alpha=0.5)
    ax.bar(np.add(x[37:40], 0.25), nao_plus[37:40], align='center', width=.5,  color='red', hatch="//", alpha=0.5)
    ax.bar(np.add(x[37:40], 0.25), nao_minus[37:40], align='center', width=.5, color='blue', hatch="//", alpha=0.5)


def pdo_assim(fig_id):
    fn = 'data/pdo_assim.nc'
    f = netcdf.netcdf_file(fn, 'r')
    pdo =  np.array(f.variables['pca_princ'].data)[:,0]
    time = np.array(f.variables['time'].data).squeeze()
    cal_start = datetime.strptime('1960-01-01', '%Y-%m-%d')
    timelabels = []
    for val in time:
        tmp_date = cal_start + timedelta(days=val)
        timelabels.append(datetime.strftime(tmp_date, '%Y'))
    timelabels.append('2015')

    ax = plt.subplot(*fig_id)
    pdo_plus = np.ma.masked_less(pdo, 0)
    pdo_minus = np.ma.masked_greater(pdo, 0)

    x = range(0, len(pdo_plus))
    ax.bar(x[:13], pdo_plus[:13], align='center', width=1., color='red')
    ax.bar(x[:13], pdo_minus[:13], align='center', width=1., color='blue')
    ax.bar(np.add(x[13:16], -0.25), pdo_plus[13:16], align='center', width=.5, color='red')
    ax.bar(np.add(x[13:16], -0.25), pdo_minus[13:16], align='center', width=.5, color='blue')
    ax.bar(x[16:35], pdo_plus[16:35], align='center', width=1., color='red')
    ax.bar(x[16:35], pdo_minus[16:35], align='center', width=1., color='blue')

    ax.bar(x[35:37], pdo_plus[35:37], align='center', width=1., color='red')
    ax.bar(x[35:37], pdo_minus[35:37], align='center', width=1., color='blue')
    ax.bar(np.add(x[37:40], -0.25), pdo_plus[37:40], align='center', width=.5, color='red')
    ax.bar(np.add(x[37:40], -0.25), pdo_minus[37:40], align='center', width=.5, color='blue')
    ax.bar(x[40:48], pdo_plus[40:48], align='center', width=1., color='red')
    ax.bar(x[40:48], pdo_minus[40:48], align='center', width=1., color='blue')

    ax.set_xticks([0, 12, 24, 36])
    ax.set_xticklabels(timelabels[::12] + ['2015'])
    ax.axvline(x[10], color='black')
    ax.axvline(x[34], color='black')
    ax.axis([-0.5, len(x) - .5, -50, 50])
    ax.set_title('PDO')
    ax.set_xlabel('Time')

    fn = 'data/pdo_forecast.nc'
    f = netcdf.netcdf_file(fn, 'r')
    pdo = np.array(f.variables['pca_princ'].data).squeeze()[:, 0]
    pdo *= -1
    time = np.array(f.variables['time'].data).squeeze()
    cal_start = datetime.strptime('1961-01-01', '%Y-%m-%d')
    timelabels = []
    for val in time:
        tmp_date = cal_start + timedelta(days=val)
        timelabels.append(datetime.strftime(tmp_date, '%m-%Y'))
    pdo_plus = np.ma.masked_less(pdo, 0)
    pdo_minus = np.ma.masked_greater(pdo, 0)
    x = range(0, len(pdo))
    ax.bar(np.add(x[13:16], 0.25), pdo_plus[13:16], align='center', width=.5, color='red', hatch="//", alpha=0.5)
    ax.bar(np.add(x[13:16], 0.25), pdo_minus[13:16], align='center', width=.5, color='blue', hatch="//", alpha=0.5)
    ax.bar(np.add(x[37:40], 0.25), pdo_plus[37:40], align='center', width=.5, color='red', hatch="//", alpha=0.5)
    ax.bar(np.add(x[37:40], 0.25), pdo_minus[37:40], align='center', width=.5, color='blue', hatch="//", alpha=0.5)


aod((1, 3, 1))
nao_assim((1, 3, 2))
pdo_assim((1, 3, 3))
plt.show()

