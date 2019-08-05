'''
This file creates a calibration plot that is used to calculate calibration coefficents (slope and intercept)
'''

from scipy import stats
import matplotlib.pyplot as plt
import numpy as np 





def Calibration_Curve(ADC,ADC_loc,EN,Error,N,title,detector):
    
    import time
    date_string = time.strftime("%Y-%m-%d-%H:%M")

    slope, intercept, r_value, p_value, std_err = stats.linregress(EN,ADC) #preforms linear regression(fit) for ADC location and expected peak energies. 
    

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


    adc = ADC_loc
    

    plt.figure(figsize=(9.0,8.0))
    
    # You can Modify the code below to change the formating of the calibration curve. 
    
    plt.errorbar(EN,adc,yerr=Error,fmt ='o')
    plt.plot(l,fit,label='y={:.2f}x + {:.2f}'.format(slope,intercept))
    plt.title(title)
  
    plt.ylabel('ADC Location')
    plt.xlabel('Energy [keV]')
    #plt.xlim(0,2500)
    plt.grid(which='major',axis= 'both',linestyle='--')
    plt.legend()
    plt.savefig('Data/'+str(detector)+'/Figures/'+str(title))
    plt.show()

    print('Slope =',slope, 'Intercept =', intercept, 'error =', std_err)
    
    

    return slope,intercept,r_value




#This kind of works. Needs to be tweeked. 
def Calibration_Curve_Quadractic(ADC,ADC_loc,EN,Error,N):

    slope, intercept, r_value, p_value, std_err = stats.linregress(ADC,EN)
    z = np.polyfit(ADC,EN,2)

    fit = []

    l = np.arange(0,500)

    for x in l:
        y1 = z[0]*x**2 + z[1]*x + z[2]
        fit.append(y1)

    for x in Error:
        Error = x*100


    if N == 4:
        adc = ADC_loc
    else: 
        adc = ADC_loc[:-1]
    
    

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