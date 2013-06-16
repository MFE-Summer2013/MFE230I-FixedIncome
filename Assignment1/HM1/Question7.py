'''
Created on Jun 15, 2013

@author: Billy
'''

from rates import conversion
import fileOperations

if __name__ == '__main__':
    pass

dataFileName = 'HW1_data.csv'
T, DF = fileOperations.getFile(dataFileName)

spotRatesEXP = conversion.rates(DF, T)
spotRates    = conversion.rates(DF, T, 2)
DF_EXP = conversion.getDF(spotRatesEXP, T)
DF     = conversion.getDF(spotRates,T,2)

new_T = []
for i in range(90):
    new_T.append(0.25 + 0.25*i)
    
spotRates_I, new_T = conversion.interpolate(spotRates, T, new_T)
forwardRates = conversion.getFowardRates(DF, T, 2);

DF_I = conversion.getDF(spotRates_I, new_T, 2);
forwardRates_I = conversion.getFowardRates(DF_I,new_T,2)

parcurve, parcurve_T = conversion.parYield(DF, T, 2);
parforward, parfowrad_T = conversion.parYield_forward(5, DF, T, 2);

import matplotlib.pyplot as plt
plt.plot(T, spotRates, 'b', new_T, spotRates_I,'r')
plt.figure(2)
plt.plot(T,forwardRates,'b', new_T, forwardRates_I,'r')
plt.figure(3)
plt.plot(T,spotRates,'b', parcurve_T, parcurve,'g',parfowrad_T, parforward,'r')
plt.show()
