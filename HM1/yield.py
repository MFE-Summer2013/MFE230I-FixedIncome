'''
Created on Jun 17, 2013

@author: Billy
'''

import math as m

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

    def getForwardRates(self, feq=-1):
        forwardRates = []
        if feq == -1:
            for t, df, i in zip(self.T, self.Df, range(len(self.T))):
    