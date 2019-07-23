"""
Reference for Scipy.signal: https://docs.scipy.org/doc/scipy/reference/signal.html
"""

import numpy as np
from scipy.signal import find_peaks,peak_widths,peak_prominences
from fit_peak import * 
from Calibration_Curve import * 
import pandas as pd 


def Peak_locate(y, dis,prom,width,bincenters,N,label):
    
    """
    The parameters below will need to be adjusted depending on the source you are using. You will need to look at the inital histogram to make
    a guess for the parameters. IF you're using Na22. The parameters should need not be adjusted. 
    
    Y = histogrammed data. 
    dis = distance between peaks. Will only look at peaks that are further apart than 'distance'
    prom = 'height' of peak. Only looks at peaks with a height greater than 'prominance'
    wid = minimum width of peaks to look for. Only looks at peaks with a width greater than 'width'
    """

    Y = y
    peaks, properties = find_peaks(Y,distance = dis,prominence=prom,width=width) 
     

    widths = peak_widths(Y, peaks) #inital peak width guess 

    amp = y[peaks] #intial peak amplitude guess 

    ADC_loc = [] # inital peak location guess 
    for x in peaks: 
        a = bincenters[x]
        ADC_loc.append(a)

    
  
    ADC_fit = []
    Error = []

    """
    The for loop below uses the parameters found above to pass into a fitting alogrithm. fit_peak is located in fit_peak.py. 
    """
    for i in np.arange(N):
        params = [amp[i],ADC_loc[i],widths[0][i],0,1]
        results, fit = fit_peak(bincenters, y,params,label)

        x = fit.params['cen'].stderr #error in the peak location (central value) returned from fit_peak
        Error.append(x)      
 
        ADC_fit.append(results[1])
    
    
    print(ADC_fit)

    return ADC_loc, ADC_fit,peaks,widths,amp,fit,Error
