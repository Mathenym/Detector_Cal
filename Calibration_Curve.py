from scipy import stats
import matplotlib.pyplot as plt
import numpy as np 





def Calibration_Curve(ADC,ADC_loc,EN,Error):

    slope, intercept, r_value, p_value, std_err = stats.linregress(ADC,EN)
    

    fit = []

    l = np.arange(0,500)
    for x in l:
        y = slope*x + intercept
        fit.append(y)



    for x in Error:
        Error = x*100

    
    adc = ADC_loc 

    plt.figure(figsize=(9.0,8.0))

    plt.errorbar(EN,adc,yerr=Error,fmt ='o')
    plt.plot(fit,l,label='y={:.2f}x + {:.2f}'.format(slope,intercept))
    plt.title('Calibration Curve')
    plt.text(2000,110, "***Errors are multiplied by 100***")
    plt.ylabel('ADC Location')
    plt.xlabel('Energy [keV]')
    plt.grid(which='major',axis= 'both',linestyle='--')
    plt.legend()
    plt.show()

    print('Slope =',slope, 'Intercept =', intercept, 'error =', std_err)

    return slope,intercept



def Calibration_Curve_Quadractic(ADC,ADC_loc,EN,Error):

    slope, intercept, r_value, p_value, std_err = stats.linregress(ADC,EN)
    z = np.polyfit(ADC,EN,2)

    fit = []

    l = np.arange(0,500)

    for x in l:
        y1 = z[0]*x**2 + z[1]*x + z[2]
        fit.append(y1)

    for x in Error:
        Error = x*100

    
    adc = ADC_loc

    plt.figure(figsize=(9.0,8.0))
    plt.errorbar(EN,adc,yerr=Error,fmt ='o')
    plt.plot(fit,l, label = 'y={:.2f}x^2 +{:.2f}x +{:.2f}'.format(z[0],z[1],z[2]))
    plt.title('Calibration Curve')
    plt.text(2000,110, "***Errors are multiplied by 100***")
    plt.ylabel('ADC Location')
    plt.xlabel('Energy [keV]')
    plt.grid(which='major',axis= 'both',linestyle='--')
    plt.legend()
    plt.show()

    return z