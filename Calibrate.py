#%%
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
import seaborn as sns 
import matplotlib as mpl
mpl.rcParams.update(_VSCode_defaultMatplotlib_Params)
sns.set_style(rc = {'figure.facecolor':'white'})
import numpy as np
import uproot 
import matplotlib.pyplot as plt
from scipy.signal import find_peaks,peak_widths,peak_prominences
from scipy import stats
from fit_peak import * 
from pylab import *
from scipy.optimize import curve_fit
import pandas as pd 

from Peak_find import * 
from Calibration_Curve import * 
from Calibration_Equations import *

#%%
Energy1 = []
for arrays in uproot.iterate("~/Desktop/multi_run/*.root","Data_F;1","Energy",outputtype=list):
    
    for x in arrays:
        Energy1.extend(x)
        
bin = np.arange(0,max(Energy1))
y,binedges = np.histogram(Energy1,bin)
bincenters = 0.5*(binedges[1:]+binedges[:-1])


#%%
N = 3
ADC_loc, ADC_fit,peaks,widths,amp,fit,Error = Peak_locate(y,bincenters,N)


#%%

EN1 = [511,1274,1785] #where peaks should be in keV
EN2 = [511,1274,1785,2614] #where peaks should be in keV
if N ==3: 
        EN = EN1
else: 
        EN = EN2

#%%
print(ADC_loc)

#%%


slope,intercept = Calibration_Curve(ADC_fit,ADC_loc,EN,Error,N)

#z = Calibration_Curve_Quadractic(ADC_fit,ADC_loc,EN,Error)

#%%

d1,bincenter1,width,mean,amplitude,wid_error = Calibrate_linear(Energy1,ADC_loc,peaks,widths,bin,slope,intercept)



#%%
#df2, bincenter2 = Calibrate_Quadratic(Energy1,ADC_loc,peaks,widths,bin,z)

#%%


plt.figure(figsize=(9.0,8.0))
plt.plot(bincenters,y,label = 'Spectrum')


plt.xlim(60,450)
plt.ylim(1,10**8)
plt.yscale('log')
plt.title('Uncalibrated Spectrum for Na22 Det_65008-01994')
plt.xlabel("ADC")
plt.ylabel("Count ")
plt.grid(linestyle='-', linewidth=0.35)
plt.legend() 

plt.show()


#%%

plt.figure(figsize=(9.0,8.0))
plt.plot(bincenter1,d1,label = 'Spectrum')

EN1 = [511,1274,1785,2614]
for x in EN1:
        plt.vlines(x,0,10**9,linestyle='--', linewidth=0.7)

plt.xlim(0,3000)
plt.ylim(1,10**8)
plt.yscale('log')
plt.title('Calibrated Energy Spectrum for Na22 Det_65008-01994')
plt.xlabel("Energy [keV]")
plt.ylabel("Count ")
plt.grid(linestyle='-', linewidth=0.35)
plt.legend() 

plt.show()




#%%
Mean =[]

for x in mean: 
       m = float("{0:.2f}".format(x))
       Mean.append(m)

print('Expected peak location in Energy is: ',EN)
print('Fitted peak location in Energy is: ',Mean)


for c,e in zip(Mean,EN):

        percent_diff = np.abs(c-e)/(e) * 100
        print('Percent Difference in the mean for ' +str(e)+' is: ',"{0:.2f}".format(percent_diff),'%')


for w,e,er in zip(width,EN,wid_error):
        FWHM = 2*w*np.sqrt(np.log(2))
        res = FWHM/(e) * 100 
        print('FWHM for ' +str(e)+ ' keV is: ' ,"{0:.2f}".format(FWHM),'±',"{0:.2f}".format(er))
        print('Pulse Height Resolution for ' +str(e)+ ' keV is: ' ,"{0:.2f}".format(res),'%')



#%%


#%%
