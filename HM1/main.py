

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
plt.figure(3)
plt.plot(T_1,paryield)

print 'Testing packages'

plt.show()
