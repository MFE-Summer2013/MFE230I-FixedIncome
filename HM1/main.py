
'''
Created on Jun 18, 2013

@author: Billy
'''

import numpy as np
import readData
import yieldCurve
import matplotlib.pyplot as plt

if __name__ == '__main__':
    pass

T, DF = readData.readFile('HW1_data.csv')
myCurve = yieldCurve.YieldCurve()
myCurve.setCurve(T, DF)
myCurve.plotCurve(2);
myCurve.exportSpotRates('rates.csv', 2)

T_i = np.linspace(0,25, 25*4+1)
T_i, rates = myCurve.getInterpolatedRates(T_i, 2);

plt.plot(T_i, rates, 'r')

startT = np.linspace(0.25, 25, 25*4)
endT = startT + 0.25;

T_1, paryield = myCurve.getParYield()
T_i, for_paryield = myCurve.getParYield(5)

from IR_Models import Polynomial

myModel = Polynomial.Polynomial()
myModel.estimate(DF, T)
DF_fit =  myModel.fit(T)
rate_fit = yieldCurve.DF_to_Rates(DF_fit, T, 2)

plt.figure(4)
myCurve.plotCurve(2)
plt.plot(T, rate_fit)

plt.figure(3)
plt.plot(T_1,paryield)
plt.plot(T_i,for_paryield,'r')

plt.show()
