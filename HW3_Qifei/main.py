'''
Created on Jun 28, 2013

@author: Qifei
'''

if __name__ == '__main__':
    pass

import numpy as np
from readData import readFile
from IR_Models import Polynomial
from yieldCurve import *
from Bond import Bond
import matplotlib.pyplot as plt
from pandas import *

maturity_in_question = ['1','3','5','10','20','30']

'''
# Question 1

#Read data
T,DF = readFile('../../Assignment 1/Spreadsheet_for_problem_set_1.csv',1)
  
# Get DFs using Polynomial fit
polynomial_model = Polynomial.Polynomial()
polynomial_model.estimate(DF, T)
T = np.arange(.5,30.5,.5)
DF = polynomial_model.fit(T)
  
# Get par yield
yc = YieldCurve()
yc.setCurve(T, DF)
par_yield = yc.getParYield()
  
maturity = range(1,31)
convexity= np.zeros(30)
for i in maturity:
    convexity[i-1] = Bond(100, par_yield[1][2*i-1], i).getConvexity(yc)
      
plt.figure(1)
plt.plot(maturity,convexity, label="Convexity")
plt.ylabel('Convexity ($)')
plt.xlabel('Time to Maturity')
plt.legend(loc = 4,prop={'size':10})
  
# Question 2
bp = .01/100
spotRates = yc.getSpotRates(2)
yc_shifted = YieldCurve()
plt.figure(2)
for i, shift in enumerate(np.array([10, 300, -10, -300]) * bp):
    delta_price_approximate_D = np.zeros(30)
    delta_price_approximate_DC = np.zeros(30)
    delta_price_exact = np.zeros(30)
  
    spotRates_shifted = np.add(spotRates, shift)
    yc_shifted.setCurve(yc.T, spotRates_to_DF(spotRates_shifted, yc.T, 2))
  
    for t in maturity:
        b = Bond(100, par_yield[1][2 * t - 1], t)
        duration = b.getModDuration(yc)
        convexity = b.getConvexity(yc)
          
        delta_price_approximate_D[t - 1] = (-duration * shift) * 100  
        delta_price_approximate_DC[t - 1] = (-duration * shift + convexity * (shift) ** 2 / 2) * 100
        delta_price_exact[t - 1] = b.getBondPrice(yc_shifted) - 100
      
    plt.subplot(2, 2, i+1)
    plt.plot(maturity, delta_price_approximate_D, label="Approximated (Duration only)")
    plt.plot(maturity, delta_price_approximate_DC, label="Approximated (Duration+Convexity)")
    plt.plot(maturity, delta_price_exact, label="Exact")
    plt.title('Price Change due to %d bp parallel shift'%(shift*10000))
    plt.ylabel('Price Change ($)')
    plt.xlabel('Time to Maturity')
    plt.legend(loc=3, prop={'size':10})
'''

# Question 3
# Read data
#yields = read_csv('C:\Users\Qifei\Documents\Study\UCB\\2013 2.Summer\\230I-Fixed Income Markets\Assignments\Assignment 3\\termstruc.csv')
yields = read_csv('../termstruc.csv', index_col=[0], parse_dates=['Date'])
yields = yields[(yields.index >= '1986-01-02') & (yields.index <= '2008-12-31')]
yields = (yields/100).sort()

T = range(1,31)
'''
# (a) highest and lowest one-year rate
plt.figure(3)
plt.subplot(2,4,1)
yields.iloc[yields['1'].argmax()].plot()
plt.legend(loc=2, prop={'size':10})
plt.subplot(2,4,2)
yields.iloc[yields['1'].argmin()].plot()
plt.legend(loc=2, prop={'size':10})

# (b) highest and lowest slope
slope = yields['10'] - yields['1']
plt.subplot(2,4,3)
yields.iloc[slope.argmax()].plot()
plt.legend(loc=2, prop={'size':10})
plt.subplot(2,4,4)
yields.iloc[slope.argmin()].plot()
plt.legend(loc=2, prop={'size':10})

# (c) highest and lowest convexity
convexity = 2 * yields['5'] - yields['1'] - yields['30']
plt.subplot(2,4,5)
# forward rates
yc = YieldCurve()
yc.setCurve(T, spotRates_to_DF(yields.iloc[convexity.argmax()], T))
plt.plot(yc.T, yc.getForwardRates_PeriodByPeriod(), label='Forward Rates')
plt.grid()
yields.iloc[convexity.argmax()].plot()
plt.legend(loc=4, prop={'size':10})

plt.subplot(2,4,6)
# forward rates
yc = YieldCurve()
yc.setCurve(T, spotRates_to_DF(yields.iloc[convexity.argmin()], T))
plt.plot(yc.T, yc.getForwardRates_PeriodByPeriod(), label='Forward Rates')
plt.grid()
yields.iloc[convexity.argmin()].plot()
plt.legend(loc=4, prop={'size':10})

convexity = 2 * yields['15'] - yields['1'] - yields['30']
plt.subplot(2,4,7)
# forward rates
yc = YieldCurve()
yc.setCurve(T, spotRates_to_DF(yields.iloc[convexity.argmax()], T))
plt.plot(yc.T, yc.getForwardRates_PeriodByPeriod(), label='Forward Rates')
plt.grid()
yields.iloc[convexity.argmax()].plot()
plt.legend(loc=4, prop={'size':10})

plt.subplot(2,4,8)
# forward rates
yc = YieldCurve()
yc.setCurve(T, spotRates_to_DF(yields.iloc[convexity.argmin()], T))
plt.plot(yc.T, yc.getForwardRates_PeriodByPeriod(), label='Forward Rates')
plt.grid()
yields.iloc[convexity.argmin()].plot()
plt.legend(loc=4, prop={'size':10})

# Question 4
change = (yields - yields.shift(1)).dropna()

std = []
for p in range(change.shape[0] - 60 + 1):
    std.append(change[p:p + 60].std())

std = DataFrame(data=std, index=change.index[59:])

plt.figure(4)
std[['1','3','5','10','20','30']].plot()
yields['1'][60:].plot(secondary_y=True, label='1-year spot')
plt.legend(loc=3, prop={'size':10})

# Question 5
correlation_matrix = change[maturity_in_question].corr()
print correlation_matrix 

# Question 6
eigen_value, eigen_vector = np.linalg.eig(correlation_matrix)

plt.figure(5)
plt.plot(maturity_in_question,eigen_vector[:,0], label='First')
plt.plot(maturity_in_question,eigen_vector[:,1], label='Second')
plt.plot(maturity_in_question,eigen_vector[:,2], label='Third')
plt.legend(loc=2)
plt.xlabel('Maturity')
plt.ylabel('Loadings')

'''
# Question 7

fwd_rates = DataFrame(data=yields)
yc = YieldCurve()
for t in yields.index:
    yc.setCurve(T, spotRates_to_DF(yields.loc[t], T))
    fwd_rates.loc[t] = yc.getForwardRates_PeriodByPeriod()

# repeat: Question 4
fwd_change = (fwd_rates - fwd_rates.shift(1)).dropna()

fwd_std = []
for p in range(fwd_change.shape[0] - 60 + 1):
    fwd_std.append(fwd_change[p:p + 60].std())

fwd_std = DataFrame(data=fwd_std, index=fwd_change.index[59:])

#plt.figure(6)
fwd_std[maturity_in_question].plot()
yields['1'][60:].plot(secondary_y=True, label='1-year spot')
plt.legend(loc=3, prop={'size':10})

# repeat: Question 5
fwd_correlation_matrix = fwd_change[maturity_in_question].corr()
print fwd_correlation_matrix

# repeat: Question 6
fwd_eigen_value, fwd_eigen_vector = np.linalg.eig(fwd_correlation_matrix)

plt.figure(7)
plt.plot(maturity_in_question,fwd_eigen_vector[:,0], label='First')
plt.plot(maturity_in_question,fwd_eigen_vector[:,1], label='Second')
plt.plot(maturity_in_question,fwd_eigen_vector[:,2], label='Third')
plt.legend(loc=2)
plt.xlabel('Maturity')
plt.ylabel('Loadings')


plt.show()