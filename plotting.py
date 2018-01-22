import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import numpy.ma as ma

ABC_IDS = {
    1: '(a)', 2: '(b)', 3: '(c)', 4: '(d)', 5: '(e)', 6: '(f)',
    7: '(g)', 8: '(h)', 9: '(j)'
}


def plot_fldmean(ax, x_val, val1, val2, sig=None, y_range=[-0.0, .8], x_range=[-0.5, 6.5]):

    if sig is not None:
        for i in range(0, val1.shape[0]):
            if (len(sig.shape) > 0 and not sig[i]) or (len(sig.shape) == 0 and sig == False):
                ax.plot((x_val[i],x_val[i]), (val1[i], val2[i]), 'k--')

 
    ax.scatter(x_val, val1, color='blue')
    ax.scatter(x_val, val2, color='red')
    print x_range
    ax.axis(x_range + y_range)


def plot_timeseries(ax, x_val, val1, val2, min_val1=None, max_val1=None, min_val2=None, max_val2=None):

    if min_val1 is not None:
        ax.fill_between(x_val, min_val1, max_val1, color='red', alpha=.15)
    if min_val2 is not None:
        ax.fill_between(x_val, min_val2, max_val2, color='blue', alpha=.15)

    ax.plot(x_val, val1, color='red')
    ax.plot(x_val, val2, color='blue')


def get_projection(proj=None):

    if proj=='npstere':
        print 'npstere prohection'
        return Basemap(projection='npstere', boundinglat=50, lon_0=0, round=True)
    return Basemap(llcrnrlon=-247.5, llcrnrlat=-87.5, urcrnrlon=107.5, urcrnrlat=87.5) #(llcrnrlon=-177.5, llcrnrlat=-87.5, urcrnrlon=177.5, urcrnrlat=87.5)


def plot_field(ax, ar, mask=None, min_val=-1., max_val=1., projection=None, cmap=plt.cm.RdBu_r, steps=11):

    lon = np.linspace(-177.5, 177.5, 72)
    lat = np.linspace(-87.5, 87.5, 36)

    if projection=='npstere':
        step = 2.5
        lon = np.array(map(lambda i: i-2.5,lon))
        lat = np.array(map(lambda i: i-2.5,lat))
        lon = np.insert(lon,lon.shape[0],lon[-1]+2*step)
        lat = np.insert(lat,lat.shape[0],lat[-1]+2*step)
    else:
        lon = np.linspace(-247.5, 107.5, 72)

    colorSteps = np.linspace(min_val, max_val, steps)

    from ensemble_io import open_file 
    pi_fn = '/pf/b/b324057/alarm/data/pi_control/tas_Amon_MPI-ESM-LR_piControl_r1i1p1_185001-284912.nc_YM_ANOM_RM4_STD_REMAP_SELBOX'
    pi_fn = '/pf/b/b324057/alarm/data/pi_control/sic/sic_OImon_MPI-ESM-LR_piControl_r1i1p1_185001-284912.nc_MAR_ANOM_RM4_STD_REMAP_SELBOX2'
    pi_fn = '/pf/b/b324057/alarm/data/pi_control/sic/sic_OImon_MPI-ESM-LR_piControl_r1i1p1_185001-284912.nc_SEP_ANOM_RM4_STD_REMAP_SELBOX'
    pi_mask = open_file(pi_fn, 'sic')
    print ar.shape, pi_mask.shape
    #ar = np.ma.masked_where(np.absolute(ar) < 0.9 * pi_mask, ar)

    norm = mpl.colors.BoundaryNorm(colorSteps, cmap.N)
    cmap.set_bad('grey')
    m = get_projection(projection) 
    x, y = np.meshgrid(lon, lat)
    x, y = m(x, y)
    cs = m.pcolormesh(x, y, ar, cmap=cmap, norm=norm, linewidth=0, rasterized=True)
    m.drawcoastlines(ax=ax)

    sig_x = []
    sig_y = []
    if mask is not None:
        lon = lon + (lon[1]-lon[0])/2
        lat = lat + (lat[1]-lat[0])/2
        for (x, y), value in np.ndenumerate(mask):
            if not value:
                sig_x.append(lon[y])
                sig_y.append(lat[x])
                size = 9
                if m.projection == 'npstere' and lat[x] > 80:
                    size = 4
                elif m.projection == 'npstere' and lat[x] < 55:
                    size = 15
                else:
                    size = 9
                i, j = m(lon[y], lat[x])
                m.scatter(i, j, size, marker='x', color='k')
        sig_x, sig_y = m(sig_x, sig_y)
        #m.scatter(sig_x, sig_y, 9, marker='x', color='k')
    return cs


def add_number(ax, fig_id, x=-250, y=100, size=17):
    print x, y
    ax.text(x, y, ABC_IDS[fig_id], size=size)    


def add_colorbar(fig, cs, color_steps=None, label=None):
    fig.subplots_adjust(bottom=0.415)
    cbar_ax = fig.add_axes([0.125, 0.15, 0.775, 0.03])
    cbar = fig.colorbar(cs, cax=cbar_ax, orientation='horizontal', ticks=color_steps)
    if label is not None:
        cbar.ax.set_xlabel(label)


def plot_vertical(ax, ar, mask=None):
    print mask
    colorSteps = np.linspace(-1., 1., 11)
    my_cmap = plt.cm.RdBu_r
    norm = mpl.colors.BoundaryNorm(colorSteps, my_cmap.N)
    print ar.shape
    #ax = plt.subplot(2, 2, 1)
    y = [100000, 92500, 85000, 70000, 60000, 50000, 40000, 30000, 25000, 20000, 15000, 10000, 7000, 5000, 3000, 2000, 1000, 700, 500, 300, 200, 100, 40, 20, 10]
    x = range(0, ar.shape[1])
    #x, y = np.meshgrid(range(0, 25), range(0, ar.shape[1]))
    ax.set_yscale('log')
    cs = ax.pcolormesh(x, y, ar[:,:], cmap=my_cmap, norm=norm)
    #cs = ax.imshow(np.flipud(ar[:,:]), interpolation="nearest", aspect='auto', cmap=my_cmap, norm=norm)
    #plt.xticks(range(1, len(lat), 10), np.round(lat[1::10]))
    #plt.yticks(range(0, len(plev), 3), plev[0::3])
    #ax.set_title(exp1)

    #plt.suptitle('%s vs. %s - Timestep %03d' % (exp1, exp2, step))

    #fig.subplots_adjust(bottom=0.15)

    #cbar_ax = fig.add_axes([0.1, 0.05, 0.8, 0.03])
    #cbar = fig.colorbar(cs, cax=cbar_ax, orientation='horizontal', ticks=colorSteps[0::2])
    ax.autoscale(False)
    #ax.imshow(np.flipud(mask[:,:]))
    ax.set_xlabel('Latitude [degrees]')
    ax.set_ylabel("Pressure [Pa]")
    plt.gca().invert_yaxis() 
    #ax.set_xticks()
    ax.axis([0, 95, 100000, 10])
    print mask, 'THE MASK'
    if mask is not None:
        x_sig = list()
        y_sig = list()
        for i in range(0, mask.shape[0]):
            for j in range(0, mask.shape[1]):
                if not mask[i,j]:
                    x_sig.append(j+0.5)
                    try:
                        y_sig.append(y[i]+(y[i]-y[i+1])/2)
                    except:
                        y_sig.append(8)

        ax.scatter(x_sig, y_sig, 7, marker='x', color='black')
    return cs
    #plt.savefig('%s/fig%03d.png' % (output, step))
    #print 'Saved %s/fig%03d.png' % (output, step)
    #plt.close(fig)


class AxesFormatter(object):

    def __init__(self, xticks, yticks=None, xlabel=None, ylabel=None, xticklabels=None, title=None, show_legend=True, yticklabels=None):
        self.xticks = xticks
        self.yticks = yticks
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xticklabels = xticklabels
        self.yticklabels = yticklabels
        self.show_legend = show_legend
        self.title = title

    def __call__(self, ax):

        ax.set_ylabel(self.ylabel)
        ax.set_xlabel(self.xlabel)
        ax.set_xticks(self.xticks)
        if self.yticks is not None:
            ax.set_yticks(self.yticks)
        if self.xticklabels:
            ax.set_xticklabels(self.xticklabels)
        if self.yticklabels:
            ax.set_yticklabels(self.yticklabels)
        if self.title is not None:
            ax.set_title(self.title, y=1.04)
        if self.show_legend:
            blue_patch = mpl.patches.Patch(color='blue', label='Baseline1')
            red_patch = mpl.patches.Patch(color='red', label='Pinatubo')
            ax.legend(handles=[blue_patch, red_patch], loc='lower right')
        





