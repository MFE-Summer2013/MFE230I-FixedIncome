'''
Created on Jun 15, 2013

@author: Billy
'''

import fileOperations
from IR_Models import NelsonSiegel
from IR_Models import Svensson
from rates import conversion as cv

print "This is the file for Question 9 and 10"

dataFileName = 'HW1_data.csv'
T, DF = fileOperations.getFile(dataFileName)
spotRates = cv.rates(DF, T)

NS = NelsonSiegel.NelsonSiegel([0,0,0,0,0]);
NS.estimateCurve([0.04,0.02,0.03,1,1], (T,spotRates))
print NS.param

SV = Svensson.Svensson([0,0,0,0,0,0])
SV.estimateCurve([0.04, 0.02,0.03,0.6,1,10], (T,spotRates))
print SV.param


newT30 = []
for i in range(60):
    newT30.append((i+1)*0.5)

newT60 = []
for i in range(120):
    newT60.append((i+1)*0.5)


fittedRates_NS      = NS.getYield(newT30)
fittedRates_SV      = SV.getYield(newT30)

discount_NS         = cv.getDF(fittedRates_NS, newT30)
discount_SV         = cv.getDF(fittedRates_SV, newT30)

parcurve_NS, TNS    = cv.parYield(discount_NS, newT30, -1)
parcurve_SV, TSV    = cv.parYield(discount_SV, newT30, -1)

fittedRates_NS60    = NS.getYield(newT60)
fittedRates_SV60    = SV.getYield(newT60)
discount_NS60       = cv.getDF(fittedRates_NS60, newT60)
discount_SV60       = cv.getDF(fittedRates_SV60, newT60)

forwardRate_NS60    = cv.getFowardRates(discount_NS60, newT60,-1)
forwardRate_NS60    = cv.getFowardRates(discount_SV60, newT60,-1)

import matplotlib.pyplot as plt
plt.plot(newT30, fittedRates_NS, 'b', T, spotRates,'r')
plt.figure(2)
plt.plot(newT30, fittedRates_SV, 'b', T, spotRates,'r')
plt.figure(3)
plt.plot(newT30, fittedRates_NS, 'b', TNS, parcurve_NS,'r')
plt.figure(4)
plt.plot(newT30, fittedRates_SV, 'b', TSV, parcurve_SV,'r')
plt.figure(5)
plt.plot(newT60, fittedRates_NS60, 'b', newT60, forwardRate_NS60,'r')
plt.figure(6)
plt.plot(newT60, fittedRates_SV60, 'b', newT60, forwardRate_NS60,'r')


plt.show()


