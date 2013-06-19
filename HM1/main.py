
'''
Created on Jun 18, 2013

@author: Billy
'''

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

from IR_Models import NelsonSiegel as NS
from IR_Models import Svensson as SV

myModel = NS.NelsonSiegel()
myModel.estimate([0.045, 0.02, 0.02, 0.1, 0.1], DF, T, False)
plt.figure(2)
print myModel.param
print myModel.getEstError(DF, T, False)
r_fit =  myModel.fit(T)
plt.plot(T, myCurve.getSpotRates())
plt.plot(T, r_fit)


myModel2 = SV.Svensson()
myModel2.estimate([0.045, -0.01, 0.01, 0.02, -0.2, 0.1], DF, T, False)
plt.figure(3)
print myModel2.param
print myModel2.getEstError(DF, T, False)
r_fit =  myModel2.fit(T)
plt.plot(T, myCurve.getSpotRates())
plt.plot(T, r_fit)


plt.show()
