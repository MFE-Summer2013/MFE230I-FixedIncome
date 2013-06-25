'''@package YieldCurve
Created on Jun 17, 2013
@author: Billy
@copyright: Billy, James, Viola, Tony
'''

import math as m
import numpy as np
import matplotlib.pyplot as plt
import csv


def spotRates_to_DF(rates, T, feq = -1):
    """ This function converts the spot rates to discount factors
    @param rates: spot rates
    @param T:     vector that contains the time indices
    @param feq:   compounding frequencies
        
    """
    
    DF = []
    if feq == -1:
        for r, t in zip(rates, T):
            DF.append(m.exp(-r*t))
    else:
        for r, t in zip(rates, T):
            DF.append(m.pow(1+r/feq, -feq*t))
    return DF

def DF_to_Rates(DF, T, feq=-1):
    rates = []
    if feq == -1:  ##CONTINUOUS COMPONDING RATES
        for t, df in zip(T, DF):
            rates.append(-m.log(df) / t)
    else:          ##DISCRETE COMPOUNDING RATES
        for t, df in zip(T, DF):
            rates.append((pow(df, - 1/(t*feq))-1)*feq)
    return rates

class YieldCurve(object):

    def __init__(self):
        self.DF = []
        self.T = []
    
    def setCurve(self, T, DF):
        self.DF = DF
        self.T  = T
    
    def plotCurve(self,feq = -1):
        spotRates = self.getSpotRates(feq)
        plt.plot(self.T,spotRates, label ='Spot Rates')

    def getDiscountFactor(self):
        return self.DF
    
    def getMaturityDate(self):
        return self.T
        
    def getSpotRates(self, feq=-1):
        rates = []
        if feq == -1:  ##CONTINUOUS COMPONDING RATES
            for t, df in zip(self.T, self.DF):
                rates.append(-m.log(df) / t)
        else:          ##DISCRETE COMPOUNDING RATES
            for t, df in zip(self.T, self.DF):
                rates.append((pow(df, - 1/(t*feq))-1)*feq)
        return rates

    def exportSpotRates(self, exportFileName, feq=-1):
        rates = self.getSpotRates(feq);
        with open(exportFileName, 'wb') as f:
            writer = csv.writer(f, delimiter = ',')
            writer.writerow(['Maturity', 'Spot Rates'])
            for t, r in zip(self.T, rates):
                writer.writerow([t,r])
                        
    def getForwardRates_PeriodByPeriod(self, feq=-1):
        if feq == -1:
            forwardRates = [-m.log(self.Df[0]) / self.T[0]]
            for i in range(len(self.DF)-1):
                dT = self.T[i+1] - self.T[i]
                forwardRates.append(-m.log(self.DF[i+1]/self.DF[i]) / dT)
        else:
            forwardRates = [(pow(self.DF[0], -1/self.T[0] / feq) - 1) * feq]
            for i in range(len(self.DF) -1):
                dT = self.T[i+1] - self.T[i]
                forwardRates.append((pow(self.DF[i+1]/self.DF[i], -1 / dT /feq) - 1) * feq)
        return forwardRates
    
    def getForwardRates(self,startT, endT, feq = -1):

        startT, startDF = np.asarray(self.getInterpolatedDF(startT, feq))
        endT, endDF = np.asarray(self.getInterpolatedDF(endT, feq))
        forwardDF = endDF / startDF
     
        return DF_to_Rates(forwardDF, endT - startT, feq)
    
    def getParYield(self,startT = 0):
        '''
        T_i = np.arange(0.25,self.T[-1],0.25)
        T_i, DF_i = self.getInterpolatedDF(T_i, 2)
        DF_i = np.asarray(DF_i)    
        f = lambda i: 2*(1-DF_i[i]) / np.sum(DF_i[i::-2])
        return T_i, map(f,range(len(T_i)))
        '''
        T_i = np.arange(startT + 0.5, self.T[-1]+0.5, 0.5)
        T_i, DF_i = self.getInterpolatedDF(T_i, 2)
        
        if startT == 0:
            DF_start = [1];
        else:
            startT, DF_start = self.getInterpolatedDF([startT], 2)
        
        FDF_i = np.asarray(DF_i) / DF_start[0]
        f = lambda i: 2*(1-FDF_i[i]) / np.sum(FDF_i[i::-1])
        return T_i, map(f, range(len(T_i)))
        
    def getInterpolatedRates(self, T_int, feq = -1):
        '''
        Assume that the interpolate points T_int are in increasing order
        '''
        rates = self.getSpotRates(feq) ## Get the current rates
        newT = []
        newrates = []
        i = 1;
        for t in T_int:
            if t < self.T[0]:
                continue
            while i < len(self.T) and not(self.T[i-1] <= t < self.T[i]):
                i += 1
            if i == len(self.T):
                break
            range_int = self.T[i] - self.T[i-1]
            new_r = (rates[i] * (t - self.T[i-1]) + rates[i-1] * (self.T[i] - t)) / range_int
            newT.append(t)
            newrates.append(new_r)
        return newT, newrates 
        
    def getInterpolatedDF(self, T_int, feq = -1):
        newT, newrates = self.getInterpolatedRates(T_int, feq)
        newDF = spotRates_to_DF(newrates, newT, feq)
        return newT, newDF
        
                