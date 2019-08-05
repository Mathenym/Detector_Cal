'''
This function takes in inital peak parameters (params) and uses them as inital guesses for the following code: 

Documenation of 'lmfit' can be found here: https://lmfit.github.io/lmfit-py/index.html
'''

from lmfit.models import PowerLawModel, ExponentialModel, GaussianModel
from lmfit import Model
import numpy as np
import matplotlib.pyplot as plt
from math import exp

def fit_peak(bincenters,y,params,weights,input):
    
    
    x = bincenters 
    # sets region to fit. Determined by taking the peak location 'params[1]' and adding and subtracting the two times the width of the peak 'params[2]' and removing data outside that interval. 
    cut1 = int(params[1]+2*params[2])
    cut2 = int(params[1]-2*params[2])
    cut = (x>cut2)&(x<cut1)
    
    
    #Models to fit peaks with. Each peak is approxiamtly gaussian, but as the amount of data decreases with increasing energy, a line is also used to account for the slope of the spectrum.  
    
    def gaussian(x, amp, cen, wid):
        """1-d gaussian: gaussian(x, amp, cen, wid)"""
        return amp * np.exp(-(x-cen)**2 / (2*wid**2)) 

    def line(x, slope, intercept):
        """a line"""
        return slope*x + intercept

    
    mod = Model(gaussian) + Model(line)

    #takes parameters and uses them as initial guesses for the fit. 
    pars = mod.make_params(amp = params[0],cen = params[1],wid = params[2],slope=params[3],intercept = params[4])

    #fits each peak in a region defined by lines 18-20.
    fit = mod.fit(y[cut],pars,weights= weights[cut], x=x[cut])

    
    #plots
    
    plt.figure(figsize = (9.0,8.0))
    plt.plot(x, y,label = "Peak")
    plt.plot(x[cut], fit.best_fit, 'r--',label = 'Best Fit')
    plt.yscale('log')
    #plt.ylim(params[0]-1000,params[0]+1000)
    
    
    #As this is used before and after the calibration, the plot label will depend on the input to this function
    if input == 'ADC':
        label = 'ADC Channel'
        lower = params[1]-2*params[2]
        upper = 2*params[2]+params[1]
    else:
        label = 'Energy [keV]'       
        lower = params[1]-2*params[2]
        upper = 2*params[2]+params[1]
        
    
    plt.xlim(lower,upper)
    plt.xlabel(label)
    plt.ylabel("Count ")
    plt.grid(linestyle='-', linewidth=0.35)
    plt.legend() 



    plt.show()
    
    parameters = []
    for key in fit.params:
        #print(key, "=", "{0:.2f}".format(fit.params[key].value), "+/-", "{0:.2f}".format(fit.params[key].stderr))
        parameters.append(fit.params[key].value)

    return parameters,fit
