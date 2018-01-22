from significance import calc_sig, calc_sig_of_difference
from ensemble_io import open_ensemble
from plotting import add_number

import matplotlib.pyplot as plt
import numpy as np


class ForecastCalculator(object):

    axes = {}

    def __init__(self, variable, rows, cols, plot, pre_proc, y_text=0.73):
        self.variable = variable
        self.rows = rows
        self.cols = cols
        self.plot = plot
        self.pre_proc = pre_proc
        self.y_text = y_text

    def add_difference_subplot(self, data1, data2, timestep, fig_id):
        pina2012_array = open_ensemble(data1, self.variable, self.pre_proc)
        decs4e2012_array = open_ensemble(data2, self.variable, self.pre_proc)
        diff_2012, sig_mask, var_2012 = calc_sig(decs4e2012_array, pina2012_array)
        ax = plt.subplot(self.rows, self.cols, fig_id)
        add_number(ax, fig_id)
        self.axes[fig_id] = ax
        self.cs = self.plot(ax, diff_2012[timestep,:,:], sig_mask[timestep,:,:])
        return (diff_2012, var_2012,)

    def add_double_difference_subplot(self, data1, variance1, data2, variance2, timestep, fig_id):
        '''
        calc significance of difference
        use s_diff**2 = s_1**2 + s_2**
        '''
        diff_all, diff_masked = calc_sig_of_difference(data1, data2, variance1, variance2)
        ax = plt.subplot(self.rows, self.cols, fig_id)
        add_number(ax, fig_id)
        self.axes[fig_id] = ax
        self.cs = self.plot(ax, diff_all[timestep,:], diff_masked[timestep,:].mask)

    def add_difference_subplot_fldmean(self, data1, data2, fig_id):
        pina2014_array = open_ensemble(data1, self.variable, self.pre_proc)
        decs4e2014_array = open_ensemble(data2, self.variable, self.pre_proc)
        diff_2014, sig_mask, var_2014 = calc_sig(decs4e2014_array, pina2014_array)
        ax = plt.subplot(self.rows, self.cols, fig_id)
        add_number(ax, fig_id, x=-0.3, y=self.y_text, size=15)
        self.axes[fig_id] = ax
        x_val = range(0, decs4e2014_array.shape[1])
        print decs4e2014_array.shape, pina2014_array.shape
        print np.mean(decs4e2014_array, axis=0)
        print np.mean(pina2014_array, axis=0)
        self.plot(ax, x_val, np.mean(decs4e2014_array, axis=0), np.mean(pina2014_array, axis=0), sig_mask)
        
        if hasattr(self, 'formatter'):
            self.formatter(ax)


class TimeSeriesCalculator(ForecastCalculator):

    def add_timeseries_subplot(self, data1, data2, fig_id):
        data1_array = open_ensemble(data1, self.variable, self.pre_proc)
        data2_array = open_ensemble(data2, self.variable, self.pre_proc)
        
        ax = plt.subplot(self.rows, self.cols, fig_id)
        self.axes[fig_id] = ax
        min_val1 = np.min(data1_array, axis=0)
        max_val1 = np.max(data1_array, axis=0)
        min_val2 = np.min(data2_array, axis=0)
        max_val2 = np.max(data2_array, axis=0)
        x_val = range(0, data1_array.shape[1])
        self.plot(ax, x_val, np.mean(data1_array, axis=0), np.mean(data2_array, axis=0), min_val1, max_val1, min_val2, max_val2)
 
        if hasattr(self, 'formatter'):
            self.formatter(ax)



