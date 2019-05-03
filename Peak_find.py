import numpy as np
from scipy.signal import find_peaks,peak_widths,peak_prominences
from fit_peak import * 
from Calibration_Curve import * 
import pandas as pd 


def Peak_locate(y,bincenters,N):

    Y = y
    peaks, properties = find_peaks(Y,distance = 65,prominence =10**3,width = [0,18])
    peaks1,properties1 = find_peaks(Y)

    widths = peak_widths(Y, peaks) #inital peak width guess 

    amp = y[peaks] #intial peak amplitude guess 

    ADC_loc = [] # inital peak location guess 
    for x in peaks: 
        a = bincenters[x]
        ADC_loc.append(a)

    
    array = np.empty([3,5])
    ADC_fit = []
    dat = []
    Err = np.array([])
    for i in np.arange(N):
        params = [amp[i],ADC_loc[i],widths[0][i],0,1]
        results, fit = fit_peak(bincenters, y,params)

        x = fit.params['cen'].stderr
        dat.append(x)      
 



        ADC_fit.append(results[1])
    print(ADC_fit)

    return ADC_loc, ADC_fit,peaks,widths,amp,fit,dat
