"""
The purpose of this code is to used the calibration coefficents found in "Calibratio_Curve.py" and 'calibrates' them. This is done by running the uncalibrated data through a linear equation. 

The calibrated energy spectrum is then used to located the new peak locations in units of keV. The new peak locations, amplitudes, and widths are used as initial guesses for the peak fitting algorithim. 
"""



from fit_peak import * 


def Calibrate_linear(Energy1,ADC_loc,peaks,widths,bin,slope,intercept,input,title,detector):

    EN = [511,1274,1785,2614]

    # This takes parameters found from the first round of fitting, and runs them through the calibration equation. This effectivly puts everything in units of keV 
    E = np.array(Energy1)
    E1_cal = slope*E + intercept #calibrated energy
    
    cal_bin1 = slope*bin + intercept #takes bin selected in beggining of calibration and converts them into units of keV 
    d1,binedge1 = np.histogram(E1_cal,cal_bin1)       
    bincenter1 = 0.5*(binedge1[1:]+binedge1[:-1])
    
    cal_peak1 = slope*peaks + intercept #calibrated peak location
    cal_width1 = slope*widths[0] #calibrated peak width 
    
    print(cal_peak1)


    amps1 = d1[peaks]

    import time
    date_string = time.strftime("%Y-%m-%d-%H:%M")
    
    
    plt.figure(figsize=(9.0,8.0))
    plt.plot(bincenter1,d1,label = 'Spectrum')
    #plt.plot(bincenter2,d2,label = 'Spectrum')


    EN1 = [511,1274,1785,2614]
    for x in EN1:
            plt.vlines(x,0,10**9,linestyle='--', linewidth=0.7)

    plt.xlim(250,2850)
    plt.ylim(1,10**8)
    plt.yscale('log')

    #plt.title()
    plt.title(title)

    plt.xlabel("Energy [keV]")
    plt.ylabel("Count ")
    plt.grid(linestyle='-', linewidth=0.35)
    plt.legend() 

    plt.savefig('Data/'+str(detector)+'/Figures/'+str(title)+' '+str(date_string))
    plt.show()
    
    
    
    wid = [] 
    wid_error = []
    cen = []
    amp = []
    
    
    # Takes calibrated parameters: peak amplitide, peak location, and peak width, and uses them as intial guessses for the fit_peak algorithim. 
    for i in np.arange(len(ADC_loc)):
        params1 = [amps1[i],cal_peak1[i],cal_width1[i]/2,5,10]    
        results,fit = fit_peak(bincenter1,d1,params1,input)

        print('Fit Results for the ', EN[i],'keV peak')
        for key in fit.params:
            print(key, "=", "{0:.2f}".format(fit.params[key].value), "+/-", "{0:.2f}".format(fit.params[key].stderr)) # Prints the results, and the error in the results in each fit. 
            
        #storing values to be used later.     
        wid.append(np.abs(fit.params['wid'].value))
        wid_error.append((fit.params['wid'].stderr))
        cen.append(np.abs(fit.params['cen'].value))
        amp.append(np.abs(fit.params['amp'].value))



    #print('width =', wid)

    return d1, bincenter1, wid ,cen, amp, wid_error


#Kinda works, Needs tweeking. 
def Calibrate_Quadratic(Energy1,ADC_loc,peaks,widths,bin,z,N):


    E = np.array(Energy1)
    E2_cal = z[0]*E**2 + z[1]*E + z[2] 

    cal_bin2 = z[0]*bin**2 + z[1]*bin + z[2]

    d2,binedge2 = np.histogram(E2_cal,cal_bin2)       

    bincenter2 = 0.5*(binedge2[1:]+binedge2[:-1])

    cal_peak2 = z[0]*peaks**2 + z[1]*peaks + z[2]

    cal_width2 = z[0]*widths[0]**2 + z[1]*widths[0] + z[2]


    if N == 4:
        adc = ADC_loc
    else: 
        adc = ADC_loc[:-1]

    amps2 = d2[peaks]

    for i in np.arange(len(adc)):
        params2 = [amps2[i],cal_peak2[i],cal_width2[i]/2,5,10]    
        fit_peak(bincenter2,d2,params2)

    return d2, bincenter2 