from lmfit.models import PowerLawModel, ExponentialModel, GaussianModel
from lmfit import Model
import numpy as np
import matplotlib.pyplot as plt
from math import exp

def fit_peak(bincenters,y,params):
    
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

    expon = ExponentialModel(prefix='exp_')

    mod = Model(gaussian) + Model(line)
    #pars = mod.make_params(amp=870314, cen=94.5, wid=9, exp_amplitude=5, exp_decay=10)
    pars = mod.make_params(amp = params[0],cen = params[1],wid = params[2],slope=params[3],intercept = params[4])

    fit = mod.fit(y[cut],pars, x=x[cut])


    
   


    #print(result.fit_report([1]))

    plt.plot(x, y)
    plt.plot(x[cut], fit.best_fit, 'r--')
    plt.yscale('log')
    plt.ylim(0,10**6)
    plt.xlim(params[1]-1.5*params[2],1.5*params[2]+params[1])

    plt.show()
    
    parameters = []
    for key in fit.params:
        print(key, "=", "{0:.2f}".format(fit.params[key].value), "+/-", "{0:.2f}".format(fit.params[key].stderr))
        parameters.append(fit.params[key].value)

    return parameters
