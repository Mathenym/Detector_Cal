'''

Documentation Locations: 

uproot:        https://github.com/scikit-hep/uproot
Scipy.signal:  https://docs.scipy.org/doc/scipy/reference/signal.html
lmfit:         https://lmfit.github.io/lmfit-py/index.html


'''
    

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks,peak_widths,peak_prominences
from scipy import stats
from pylab import *
from scipy.signal import find_peaks,peak_widths,peak_prominences
from lmfit.models import PowerLawModel, ExponentialModel, GaussianModel
from lmfit import Model


def Peak_locate(y, dis,prom,width,bincenters):
    
    """
    The parameters below will need to be adjusted depending on the source you are using. You will need to look at the inital histogram to make
    a guess for the parameters. IF you're using Na22. The parameters should need not be adjusted. 
    
    Parameters: 
    
    Y: histogrammed data. 
    dis: distance between peaks. Will only look at peaks that are further apart than 'distance'
    prom: 'height' of peak. Only looks at peaks with a height greater than 'prominance'
    wid: minimum width of peaks to look for. Only looks at peaks with a width greater than 'width'
    bincenters: x-axis values returned from histogramming the data spectrum
    """
    
    Y = y
    peaks, properties = find_peaks(Y,distance = dis,prominence=prom,width=width) 
     

    widths = peak_widths(Y, peaks) #inital peak width guess 

    amp = y[peaks] #intial peak amplitude guess 

    ADC_loc = [] # inital peak location guess 
    for x in peaks: 
        a = bincenters[x]
        ADC_loc.append(a)
        

    return ADC_loc,peaks,widths,amp






def fit_peak(bincenters,y,params,weights,input):
    
    '''
    The purpose of this fucntion is to take in the parameters found from peak_find and use them as inital guesses for lmfits' peak fitting algorithm. 
    This function will fit a peak, plot the fit, and return the fit statistcs and best fit parameters.
    
    Parameters:
    
    bincenters: x-axis values returned from histogramming the data spectrum
    y_values: y-axis data from spectrum histrogram 
    params: list of values representing inital guess values for model in the following order: (peak_amplitude,peak_center,peak_width,intercept,slope)
    weights: list representing uncertainty in the y-values of the inital data set. Used to perform weighted least squares. 
    input: string representing type of data. Either 'ADC Channel' or 'Energy [keV]' 
    '''
    
    
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

    return fit





def Calibration_Curve(ADC_center,Error,EN,N,title,detector):
    
    '''
    Purpose of this function is to examin the relationship between ADC-channel location and the corresponding energy in [keV]
    
    Parameters: 
    
    ADC_center: location of peak center or 'mean value' in ADC
    Error:  Error in ADC_center location
    EN: Expected peak location in units of energy [keV]
    detector: which detector is being use. Used for plot title label. 
    
    '''
    


    slope, intercept, r_value, p_value, std_err = stats.linregress(EN,ADC_center) #preforms linear regression(fit) for ADC location and expected peak energies. 
    

    fit = []
    
    # easy plot scaling
    if N == 2: 
        l = np.arange(0,200)
    elif N == 3:
        l = np.arange(0,2000)
    elif N == 4:
        l = np.arange(0,3500)
    
    #creates array that represents line of best fit. 
    for x in l:
        y = slope*x + intercept
        fit.append(y) 

    for x in Error: #Errors are really small 
        Error = x*100
    
    # Make Plot 
    
    plt.figure(figsize=(9.0,8.0))
        
    plt.errorbar(EN,ADC_center,yerr=Error,fmt ='o')
    plt.plot(l,fit,label='y={:.2f}x + {:.2f}'.format(slope,intercept))
    plt.title(title)
  
    plt.ylabel('ADC Location')
    plt.xlabel('Energy [keV]')
    #plt.xlim(0,2500)
    plt.grid(which='major',axis= 'both',linestyle='--')
    plt.legend()
    plt.savefig('Data/'+str(detector)+'/Figures/'+str(title))
    plt.show()


    
    #Returns slope and intercept required for energy calibration. 
    
    Slope = 1/slope
    Intercept = -intercept/slope
    
    print('Slope =',Slope, 'Intercept =', Intercept, 'error =', std_err)

    return Slope,Intercept,r_value





def Calibrate_linear(Energy1,ADC_center,peaks,widths,bin,slope,intercept):


    #number type nonsese 
    
    ADC_cen = []
    for x in ADC_center:
        ADC = int(x)
        ADC_cen.append(ADC)

    # This takes parameters found from the first round of fitting, and runs them through the calibration equation. This effectivly puts everything in units of keV 
    E = np.array(Energy1)
    En_calibrated = slope*E + intercept #calibrated energy
    
    Bins_calibrated = slope*bin + intercept #takes bin selected in beggining of calibration and converts them into units of keV 
    y1,binedge = np.histogram(En_calibrated,Bins_calibrated)       
    bincenters = 0.5*(binedge[1:]+binedge[:-1])
    
    
    Mean = slope*np.array(ADC_cen) + intercept #calibrated peak location
    Width = slope*widths[0] #calibrated peak width 
    
    print(Mean)

    
    Amplitude = y1[peaks] #amplitude at peak locations 
    
    Weights = 1/y1  # New weights 

    
    return y1, bincenters, Mean, Width, Amplitude, Weights 