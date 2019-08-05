"""
The purpose of this code is to used the calibration coefficents found in "Calibratio_Curve.py" and 'calibrates' them. This is done by running the uncalibrated data through a linear equation. 

The calibrated energy spectrum is then used to located the new peak locations in units of keV. The new peak locations, amplitudes, and widths are used as initial guesses for the peak fitting algorithim. 
"""



from fit_peak import * 


def Calibrate_linear(Energy1,ADC_loc,peaks,widths,bin,Slope,Intercept):

    
    slope = 1/Slope
    intercept = -Intercept/Slope

    # This takes parameters found from the first round of fitting, and runs them through the calibration equation. This effectivly puts everything in units of keV 
    E = np.array(Energy1)
    En_calibrated = slope*E + intercept #calibrated energy
    
    Bins_calibrated = slope*bin + intercept #takes bin selected in beggining of calibration and converts them into units of keV 
    y1,binedge = np.histogram(En_calibrated,Bins_calibrated)       
    bincenters = 0.5*(binedge[1:]+binedge[:-1])
    
    Mean = slope*peaks + intercept #calibrated peak location
    Width = slope*widths[0] #calibrated peak width 
    
    print(Mean)


    Amplitude = y1[peaks] #amplitude at peak locations 
    
    Weights = 1/y1  # New weights 

    
    return y1, bincenters, Mean, Width, Amplitude, Weights 
    
    
    


