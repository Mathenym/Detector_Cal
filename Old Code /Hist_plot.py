import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from scipy.optimize import curve_fit
from scipy.signal import *
from scipy import stats

def hist_uncal(data,bin):
    
    xmin=min(data)
    xmax=max(data)

    fig,axes = plt.subplots(1,1,figsize=(9.0,8.0),sharex=True)
    ax1 = axes
    
    ax1.hist(data,bins = bin,histtype = "step",color ='blue',label = 'Data',linewidth="2")
    
    print(max(data),min(data))   
   
    ax1.set_xlabel('ADC Channel',size = '20')
    ax1.set_ylabel('Count',size = '20')
    ax1.set_title('Uncalibrated',size ='20')
    ax1.set_xlim([0,800]) 
    ax1.set_yscale('log')
    ax1.grid(True)
    ax1.yaxis.grid(True,which='minor',linestyle='--')
    ax1.legend(loc=1,prop={'size':18})
    ax1.tick_params(axis='both', labelsize = '15')
    #plt.savefig('Figures/background_det01994.png')

    plt.show()
    
    
def hist_cal(data1,bin,X1,X2,Y1,Y2):
    
    xmin=min(data1)
    xmax=max(data1)

    fig,axes = plt.subplots(1,1,figsize=(9.0,8.0),sharex=True)
    ax1 = axes

    #ax1.hist(data1,bins = bin, histtype = "step",color ='blue',label = 'Data',linewidth="2")       
    #ax1.hist(data2,bins = bin, histtype = "step",color ='red',label = 'Data',linewidth="2")
   # ax1.hist(data3,bins = bin, histtype = "step",color ='green',label = 'Data',linewidth="2")
    
    x,binedge1 = np.histogram(data1,bin)
    bincenter1 = 0.5*(binedge1[1:]+binedge1[:-1])


    #print(max(data),min(data))   

        #Where sodium peaks should be: 

        

    peaks, properties = find_peaks(x,distance = 65,prominence =10**3,width = [0,18])

    prominences = peak_prominences(x, peaks)[0]
    widths = peak_widths(x, peaks, rel_height=0.5)

    print(widths[0])

    plt.figure()

 
    


        
    
    ax1.plot(bincenter1,x, linestyle = '-',label = 'Data1',linewidth = '2')

    plt.plot(peaks,x[peaks],'x')
    plt.hlines(*widths[1:], color="C2")
    plt.axvline(x=511,color='k', linestyle='--')
    plt.axvline(x=1274,color='k', linestyle='--')
    plt.axvline(x=1785,color='k', linestyle='--')
    plt.axvline(x=2614,color='k', linestyle='--')


    ax1.set_xlabel('Energy [keV]',size = '20')
    ax1.set_ylabel('Count',size = '20')
    ax1.set_title('Calibrated',size ='20')
    ax1.set_xlim([X1,X2]) 
    ax1.set_ylim([Y1,Y2])
    ax1.set_yscale('log')
    ax1.grid(True)
    ax1.yaxis.grid(True,which='minor',linestyle='--')
    ax1.legend(loc=1,prop={'size':18})
    ax1.tick_params(axis='both', labelsize = '15')
        #plt.savefig('Figures/background_det01994.png')

    plt.show()
    
    
    
    
def hist_mult(data1,data2,data3,bin):
        
    xmin=min(data1)
    xmax=max(data1)

    fig,axes = plt.subplots(1,1,figsize=(9.0,8.0),sharex=True)
    ax1 = axes

    ax1.hist(data1,bins = bin, histtype = "step",color ='blue',label = 'Data',linewidth="2")       
    ax1.hist(data2,bins = bin, histtype = "step",color ='red',label = 'Data',linewidth="2")
    ax1.hist(data3,bins = bin, histtype = "step",color ='green',label = 'Data',linewidth="2")

    #print(max(data),min(data))   

        #Where sodium peaks should be: 
    plt.axvline(x=511,color='k', linestyle='--')
    plt.axvline(x=1274,color='k', linestyle='--')
    plt.axvline(x=1785,color='k', linestyle='--')
    plt.axvline(x=2614,color='k', linestyle='--')


    ax1.set_xlabel('ADC Bin',size = '20')
    ax1.set_ylabel('Count',size = '20')
    ax1.set_title('UnCalibrated',size ='20')
    ax1.set_xlim([0,550]) 
    ax1.set_yscale('log')
    ax1.grid(True)
    ax1.yaxis.grid(True,which='minor',linestyle='--')
    ax1.legend(loc=1,prop={'size':18})
    ax1.tick_params(axis='both', labelsize = '15')
        #plt.savefig('Figures/background_det01994.png')

    plt.show()
    
    
def hist_mult_cal(data1,data2,data3,bin,X1,X2,Y1,Y2):
        
    xmin=min(data1)
    xmax=max(data1)

    fig,axes = plt.subplots(1,1,figsize=(9.0,8.0),sharex=True)
    ax1 = axes

    #ax1.hist(data1,bins = bin, histtype = "step",color ='blue',label = 'Data',linewidth="2")       
    #ax1.hist(data2,bins = bin, histtype = "step",color ='red',label = 'Data',linewidth="2")
   # ax1.hist(data3,bins = bin, histtype = "step",color ='green',label = 'Data',linewidth="2")
    
    x,binedge1 = np.histogram(data1,bin)
    bincenter1 = 0.5*(binedge1[1:]+binedge1[:-1])
    
    y,binedge2 = np.histogram(data2,bin)
    bincenter2 = 0.5*(binedge2[1:]+binedge2[:-1])
        
    z,binedge3 = np.histogram(data3,bin)
    bincenter3 = 0.5*(binedge3[1:]+binedge3[:-1])

    #print(max(data),min(data))   

        #Where sodium peaks should be: 
        

        
    
    ax1.plot(bincenter1,x,color = 'blue', linestyle = '-',label = 'Data1',linewidth = '2')
    ax1.plot(bincenter2,y,color = 'red',  linestyle = '-',label = 'Data2',linewidth = '2')
    ax1.plot(bincenter3,z,color = 'green',linestyle = '-',label = 'Data3',linewidth = '2')
    
    plt.axvline(x=511,color='k', linestyle='--')
    plt.axvline(x=1274,color='k', linestyle='--')
    plt.axvline(x=1785,color='k', linestyle='--')
    plt.axvline(x=2614,color='k', linestyle='--')


    ax1.set_xlabel('Energy [keV]',size = '20')
    ax1.set_ylabel('Count',size = '20')
    ax1.set_title('Calibrated',size ='20')
    ax1.set_xlim([X1,X2]) 
    ax1.set_ylim([Y1,Y2])
    ax1.set_yscale('log')
    ax1.grid(True)
    ax1.yaxis.grid(True,which='minor',linestyle='--')
    ax1.legend(loc=1,prop={'size':18})
    ax1.tick_params(axis='both', labelsize = '15')
        #plt.savefig('Figures/background_det01994.png')

    plt.show()