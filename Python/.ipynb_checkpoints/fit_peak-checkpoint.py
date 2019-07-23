from lmfit.models import PowerLawModel, ExponentialModel, GaussianModel
from lmfit import Model
import numpy as np
import matplotlib.pyplot as plt
from math import exp

def fit_peak(bincenters,y,params,input):
    
    x = bincenters 
    cut1 = int(params[1]+params[2])
    cut2 = int(params[1]-params[2])


    cut = (x>cut2)&(x<cut1)

    def gaussian(x, amp, cen, wid):
        """1-d gaussian: gaussian(x, amp, cen, wid)"""
        return amp * np.exp(-(x-cen)**2 / (2*wid**2)) 

    def line(x, slope, intercept):
        """a line"""
        return slope*x + intercept

    
    mod = Model(gaussian) + Model(line)

    pars = mod.make_params(amp = params[0],cen = params[1],wid = params[2],slope=params[3],intercept = params[4])


    fit = mod.fit(y[cut],pars, x=x[cut])

    plt.figure(figsize = (9.0,8.0))
    plt.plot(x, y,label = "Peak")
    plt.plot(x[cut], fit.best_fit, 'r--',label = 'Best Fit')
    plt.yscale('log')
    #plt.ylim(params[0]-1000,params[0]+1000)
    plt.xlim(params[1]-1.5*params[2],1.5*params[2]+params[1])
    
    if input == 'ADC':
        label = 'ADC Channel'
    else:
        label = 'Energy [keV]'

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
