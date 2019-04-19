from pylab import *
from scipy.optimize import curve_fit

def peak_fit(data,guess):
    

    def gaus(x,a,x0,sigma):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))


    popt,pcov = curve_fit(gaus,x,y,a,x0,sigma)
    
    print(popt)
    print(pcov)
    
    plt.plot(xc,gaus(xc,*popt),color='red',lw=3,label='model')
    plt.xscale('log')

    