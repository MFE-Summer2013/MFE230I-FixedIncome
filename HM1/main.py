
'''
Created on Jun 18, 2013

@author: Billy
'''

import numpy as np
import readData
import yieldCurve as yc
import matplotlib.pyplot as plt
import matplotlib

if __name__ == '__main__':
    pass

font = {'family' : 'Arial'}
matplotlib.rc('font', **font)

## READ DATA FROM THE FILE
T, DF = readData.readFile('HW1_data.csv')

## SET YILED CURVE
dataCurve = yc.YieldCurve()

dataCurve.setCurve(T, DF)


## QUESTION 7 - CALCULATING CURVE
plt.subplot(2,2,1)
dataCurve.plotCurve(2)
plt.ylabel('Spot Rates')
plt.xlabel('Maturity')
plt.xlabel('Starting Date')

plt.subplot(2,2,2)
startT = np.arange(0.25,25,0.25)
endT = np.arange(0.5,25.25,0.25)
forwardRates = dataCurve.getForwardRates(startT, endT, 2)
plt.plot(startT,forwardRates)
plt.ylabel('Forward Rates')

plt.subplot(2,2,3)
T_par, parYield = dataCurve.getParYield()
dataCurve.plotCurve(2)
plt.plot(T_par, parYield, label='Par Yield')
plt.ylabel('Rates')
plt.xlabel('Maturity')
plt.legend(loc = 4,prop={'size':10})

plt.subplot(2,2,4)
T_fpar, f_parYield = dataCurve.getParYield(5)
plt.plot(T_fpar, f_parYield, 'r')
plt.ylabel('Forward Par Yield, 5-year')
plt.xlabel('Maturity')

#QUESTION 8 - POLYNOMIAL MODEL

plt.figure(2)

from IR_Models import Polynomial
poly_model = Polynomial.Polynomial()
poly_model.estimate(DF, T)

fit_T = np.arange(0.5, 30, 0.5)
fit_DF = poly_model.fit(fit_T)
fitCurve = yc.YieldCurve()
fitCurve.setCurve(fit_T, fit_DF)

plt.subplot(2,2,1)
dataCurve.plotCurve(2)
fitCurve.plotCurve(2)
plt.xlabel('Maturity')
plt.ylabel('Spot Rates')

plt.subplot(2,2,2)
T_par30, paryield30 = fitCurve.getParYield()
fitCurve.plotCurve(2)
plt.plot(T_par30, paryield30, 'r', label='Par Yield')
plt.legend(loc = 4,prop={'size':10})
plt.xlabel('Maturity')
plt.ylabel('Rates')

plt.subplot(2,2,3)
fit_T = np.arange(0.5, 60, 0.5)
fit_DF = poly_model.fit(fit_T)
fitCurve = yc.YieldCurve()
fitCurve.setCurve(fit_T, fit_DF)

forwardRate60 = fitCurve.getForwardRates_PeriodByPeriod(2)
fitCurve.plotCurve(2)
plt.plot(fit_T, forwardRate60, 'r', label='Forward Rate')
plt.legend(loc = 2,prop={'size':10})
plt.xlabel('Ending Date')
plt.ylabel('Forward Rates')


#QUESTION 9 - ESTIMATING NIESON SIEGEL MODEL

plt.figure(3)
from IR_Models import NelsonSiegel as NS
init_value = [0.04, -0.02, 0.02, 0.2, 1]
ns_model = NS.NelsonSiegel()
ns_model.estimate(init_value, DF, T, False)
print ns_model.getEstError(DF, T, False)
print ns_model.param

fit_T = np.arange(0.5, 30, 0.5)
fitted_Y = ns_model.fit(fit_T)
fitted_DF = yc.spotRates_to_DF(fitted_Y, fit_T)
fitCurve.setCurve(fit_T, fitted_DF)

plt.subplot(2,2,1)
dataCurve.plotCurve(2)
fitCurve.plotCurve(2)
plt.xlabel('Maturity')
plt.ylabel('Spot Rates')

plt.subplot(2,2,2)
T_par30, paryield30 = fitCurve.getParYield()
fitCurve.plotCurve(2)
plt.plot(T_par30, paryield30, 'r', label='Par Yield')
plt.legend(loc = 4,prop={'size':10})
plt.xlabel('Maturity')
plt.ylabel('Rates')

plt.subplot(2,2,3)
fit_T = np.arange(0.5, 60, 0.5)
fitted_Y = ns_model.fit(fit_T)
fitted_DF = yc.spotRates_to_DF(fitted_Y, fit_T)
fitCurve.setCurve(fit_T, fitted_DF)

forwardRate60 = fitCurve.getForwardRates_PeriodByPeriod(2)
fitCurve.plotCurve(2)
plt.plot(fit_T, forwardRate60, 'r', label='Forward Rate')
plt.legend(loc = 3,prop={'size':10})
plt.xlabel('Ending Date')
plt.ylabel('Forward Rates')

#QUESTION 10 - ESTIMATING NIESON SIEGEL MODEL

plt.figure(4)
from IR_Models import Svensson as SV
init_value = [0.045, 0.00, 0.02, -0.2, 0.2, 0.5]
sv_model = SV.Svensson()
sv_model.estimate(init_value, DF, T, False)
print sv_model.getEstError(DF, T, False)
print sv_model.param

fit_T = np.arange(0.5, 30, 0.5)
fitted_Y = sv_model.fit(fit_T)
fitted_DF = yc.spotRates_to_DF(fitted_Y, fit_T)
fitCurve.setCurve(fit_T, fitted_DF)

plt.subplot(2,2,1)
dataCurve.plotCurve(2)
fitCurve.plotCurve(2)
plt.xlabel('Maturity')
plt.ylabel('Spot Rates')

plt.subplot(2,2,2)
T_par30, paryield30 = fitCurve.getParYield()
fitCurve.plotCurve(2)
plt.plot(T_par30, paryield30, 'r', label='Par Yield')
plt.legend(loc = 4,prop={'size':10})
plt.xlabel('Maturity')
plt.ylabel('Rates')

plt.subplot(2,2,3)
fit_T = np.arange(0.5, 60, 0.5)
fitted_Y = sv_model.fit(fit_T)
fitted_DF = yc.spotRates_to_DF(fitted_Y, fit_T)
fitCurve.setCurve(fit_T, fitted_DF)

forwardRate60 = fitCurve.getForwardRates_PeriodByPeriod(2)
fitCurve.plotCurve(2)
plt.plot(fit_T, forwardRate60, 'r', label='Forward Rate')
plt.legend(loc = 3,prop={'size':10})
plt.xlabel('Ending Date')
plt.ylabel('Forward Rates')

#QUESTION 9 - ESTIMATING NIESON SIEGEL MODEL DURATION

plt.figure(6)
from IR_Models import NelsonSiegel as NS
init_value = [0.04, -0.02, 0.02, 0.2, 1]
ns_model = NS.NelsonSiegel()
ns_model.estimate(init_value, DF, T, True)
print ns_model.getEstError(DF, T, True)
print ns_model.param

fit_T = np.arange(0.5, 30, 0.5)
fitted_Y = ns_model.fit(fit_T)
fitted_DF = yc.spotRates_to_DF(fitted_Y, fit_T)
fitCurve.setCurve(fit_T, fitted_DF)

plt.subplot(2,2,1)
dataCurve.plotCurve(2)
fitCurve.plotCurve(2)
plt.xlabel('Maturity')
plt.ylabel('Spot Rates')

plt.subplot(2,2,2)
T_par30, paryield30 = fitCurve.getParYield()
fitCurve.plotCurve(2)
plt.plot(T_par30, paryield30, 'r', label='Par Yield')
plt.legend(loc = 4,prop={'size':10})
plt.xlabel('Maturity')
plt.ylabel('Rates')

plt.subplot(2,2,3)
fit_T = np.arange(0.5, 60, 0.5)
fitted_Y = ns_model.fit(fit_T)
fitted_DF = yc.spotRates_to_DF(fitted_Y, fit_T)
fitCurve.setCurve(fit_T, fitted_DF)

forwardRate60 = fitCurve.getForwardRates_PeriodByPeriod(2)
fitCurve.plotCurve(2)
plt.plot(fit_T, forwardRate60, 'r', label='Forward Rate')
plt.legend(loc = 3,prop={'size':10})
plt.xlabel('Ending Date')
plt.ylabel('Forward Rates')

#QUESTION 10 - ESTIMATING NIESON SIEGEL MODEL - Duration

plt.figure(7)
from IR_Models import Svensson as SV
init_value = [0.045, 0.00, 0.02, -0.2, 0.2, 0.5]
sv_model = SV.Svensson()
sv_model.estimate(init_value, DF, T, True)
print sv_model.getEstError(DF, T, True)
print sv_model.param

fit_T = np.arange(0.5, 30, 0.5)
fitted_Y = sv_model.fit(fit_T)
fitted_DF = yc.spotRates_to_DF(fitted_Y, fit_T)
fitCurve.setCurve(fit_T, fitted_DF)

plt.subplot(2,2,1)
dataCurve.plotCurve(2)
fitCurve.plotCurve(2)
plt.xlabel('Maturity')
plt.ylabel('Spot Rates')

plt.subplot(2,2,2)
T_par30, paryield30 = fitCurve.getParYield()
fitCurve.plotCurve(2)
plt.plot(T_par30, paryield30, 'r', label='Par Yield')
plt.legend(loc = 4,prop={'size':10})
plt.xlabel('Maturity')
plt.ylabel('Rates')

plt.subplot(2,2,3)
fit_T = np.arange(0.5, 60, 0.5)
fitted_Y = sv_model.fit(fit_T)
fitted_DF = yc.spotRates_to_DF(fitted_Y, fit_T)
fitCurve.setCurve(fit_T, fitted_DF)

forwardRate60 = fitCurve.getForwardRates_PeriodByPeriod(2)
fitCurve.plotCurve(2)
plt.plot(fit_T, forwardRate60, 'r', label='Forward Rate')
plt.legend(loc = 3,prop={'size':10})
plt.xlabel('Ending Date')
plt.ylabel('Forward Rates')

plt.show()
