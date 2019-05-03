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
from Calibrate import *
from Peak_find import * 
from Calibration_Curve import * 

#%%
Energy1 = []
for arrays in uproot.iterate("~/Desktop/multi_run/R1/FILTERED/*.root","Data_F;4","Energy",outputtype=list):
    
    for x in arrays:
        Energy1.extend(x)
        
bin = np.arange(0,max(Energy1))
y,binedges = np.histogram(Energy1,bin)
bincenters = 0.5*(binedges[1:]+binedges[:-1])


#%%
N = 4
ADC_loc, ADC_fit,peaks,widths,amp,fit,Error = Peak_locate(y,bincenters,N)


#%%
EN = [511,1274,1785,2614] #where peaks should be in keV
slope,intercept = Calibration_Curve(ADC_fit,ADC_loc,EN,Error)

z = Calibration_Curve_Quadractic(ADC_fit,ADC_loc,EN,Error)

#%%

d1,bincenter1 = Calibrate_linear(Energy1,ADC_loc,peaks,widths,bin,slope,intercept)
#%%
df2, bincenter2 = Calibrate_Quadratic(Energy1,ADC_loc,peaks,widths,bin,z)



#%%
plt.figure(figsize=(9.0,8.0))
plt.plot(bincenter1,d1,label = 'Spectrum')


for x in EN:
        plt.vlines(x,0,10**9,linestyle='--', linewidth=0.5)

plt.xlim(0,3000)
plt.ylim(1,10**8)
plt.yscale('log')
plt.title('Calibrated Energy Spectrum Det_65008-01994')
plt.xlabel("Energy [keV]")
plt.ylabel("Count ")
plt.grid(linestyle='-', linewidth=0.35)
plt.legend() 

plt.show()


#%%



