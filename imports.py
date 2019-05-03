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