'''
Created on Jun 17, 2013

@author: Billy
'''

import math as m
import numpy as nm

class YieldCurve(object):

    def __init__(self):
        self.DF = []
        self.T = []
    
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
    
    def getInterpolatedRates(self, T_int, feq = -1):
        '''
        Assume that the interpolate points T_int are in increasing order
        '''
        currentRates = self.getSpotRates(feq) ## Get the current rates
        
        
        
        
        
                