'''
Created on Jun 15, 2013

@author: Billy
'''

import fileOperations
from rates import conversion as cv
import matplotlib.pyplot as plt
import numpy as np
import math

def createX(start_T, endT, stepsize):
    X = []
    T = []
    t = start_T
    while t <= endT:
        x = []
        for i in range(5):
            x.append(math.pow(t,i+1))
        X.append(x)
        T.append(t)
        t += stepsize
    X = np.asmatrix(X)
    return X, T

def createX_fromT(T):
    X = []
    for t in T:
        x = []
        for i in range(5):
            x.append(math.pow(t,i+1))
        X.append(x)
    return np.asmatrix(X)

    
def convertToDF(LDF):
    DF = []
    for ldf in LDF:
        DF.append(math.exp(ldf))
    return DF

dataFileName = 'HW1_data.csv'
T, DF = fileOperations.getFile(dataFileName)
spotRates = cv.rates(DF, T, 2)

logDF = []
for df in DF:
    logDF.append(math.log(df))

X = createX_fromT(T)
logDF = np.transpose(np.asmatrix(logDF))
param = np.linalg.inv(np.transpose(X)*X) * np.transpose(X) * logDF;

newX, newT = createX(0.5, 30, 0.5)
fitted_logDF = newX * param
fitted_DF = convertToDF(fitted_logDF)
fitted_spotRates = cv.rates(fitted_DF, newT, 2)
fitted_parRates, parT = cv.parYield(fitted_DF, newT, 2);

newX60, newT60 = createX(0.5, 60, 0.5)
fitted60_logDF = newX60*param
fitted60_DF = convertToDF(fitted60_logDF)
fitted60_spotRates = cv.rates(fitted60_DF, newT60, 2)
fitted60_forward = cv.getFowardRates(fitted60_DF, newT60, 2)


plt.plot(newT, fitted_spotRates,'b', T, spotRates, 'r')
plt.figure(2)
plt.plot(newT, fitted_spotRates,'b', parT, fitted_parRates, 'r')
plt.figure(3)
plt.plot(newT60, fitted60_forward, 'r', newT60,fitted60_spotRates,'b')

plt.show()

