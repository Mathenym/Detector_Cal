
from fit_peak import * 


def Calibrate_linear(Energy1,ADC_loc,peaks,widths,bin,slope,intercept):

    EN = [511,1274,1785,2614]

    E = np.array(Energy1)
    E1_cal = slope*E + intercept
    cal_bin1 = slope*bin + intercept
    d1,binedge1 = np.histogram(E1_cal,cal_bin1)       
    bincenter1 = 0.5*(binedge1[1:]+binedge1[:-1])
    cal_peak1 = slope*peaks + intercept 
    cal_width1 = slope*widths[0] - intercept


    amps1 = d1[peaks]

    wid = [] 
    wid_error = []
    cen = []
    amp = []

    for i in np.arange(len(ADC_loc)):
        params1 = [amps1[i],cal_peak1[i],cal_width1[i]/2,5,10]    
        results,fit = fit_peak(bincenter1,d1,params1)

        print('Fit Results for ', EN[i])
        for key in fit.params:
            print(key, "=", "{0:.2f}".format(fit.params[key].value), "+/-", "{0:.2f}".format(fit.params[key].stderr))
        wid.append(np.abs(fit.params['wid'].value))
        wid_error.append((fit.params['wid'].stderr))
        cen.append(np.abs(fit.params['cen'].value))
        amp.append(np.abs(fit.params['amp'].value))



    #print('width =', wid)

    return d1, bincenter1, wid ,cen, amp, wid_error



def Calibrate_Quadratic(Energy1,ADC_loc,peaks,widths,bin,z):


    E = np.array(Energy1)
    E2_cal = z[0]*E**2 + z[1]*E + z[2] 

    cal_bin2 = z[0]*bin**2 + z[1]*bin + z[2]

    d2,binedge2 = np.histogram(E2_cal,cal_bin2)       

    bincenter2 = 0.5*(binedge2[1:]+binedge2[:-1])

    cal_peak2 = z[0]*peaks**2 + z[1]*peaks + z[2]

    cal_width2 = z[0]*widths[0]**2 + z[1]*widths[0] + z[2]




    amps2 = d2[peaks]

    for i in np.arange(len(ADC_loc)):
        params2 = [amps2[i],cal_peak2[i],cal_width2[i]/2,5,10]    
        fit_peak(bincenter2,d2,params2)

    return d2, bincenter2 