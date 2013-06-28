'''
Created on Jun 21, 2013

@author: Billy
'''


import yieldCurve as ys
import numpy as np
from scipy import optimize as op
import math as m

class Bond(object):

    def __init__(self, face, c, T, feq = 2):
        '''
        Constructor
        '''
        self.face = face
        self.c = c
        self.T = T
        self.feq = feq
        
    def getBondPrice(self, curve):
        
        timeStamp = np.arange(1.0/self.feq, self.T + 1.0/self.feq, 1.0/self.feq)
        
        timeStamp, DF = curve.getInterpolatedDF(timeStamp,self.feq)
        
        
        bondPrice = DF[-1]* self.face
        for df in DF:
            bondPrice += self.face * self.c /self.feq * df
        return bondPrice;
    
    def getBondPrice_usingYTM(self, y):
        timeStamp = np.arange(1.0/self.feq, self.T + 1.0/self.feq, 1.0/self.feq)
        bondPrice = m.pow(1+y/self.feq, -timeStamp[-1]*self.feq) * self.face
        for t in timeStamp:
            bondPrice += self.face * self.c / self.feq * pow(1+y/self.feq, -t * self.feq)
        return bondPrice
        
    def getMacDuration(self, curve):
        
        bondPrice = self.getBondPrice(curve)
        
        timeStamp = np.arange(1.0/self.feq, self.T + 1.0/self.feq, 1.0/self.feq)
        timeStamp, DF = curve.getInterpolatedDF(timeStamp,self.feq)
        
        sumDuration = timeStamp[-1] * DF[-1] * self.face
        for t, df in zip(timeStamp, DF):
            sumDuration += t * df * self.face * self.c / self.feq
        return sumDuration / bondPrice;
    
    def getModDuration(self, curve):

        MacDuration = self.getMacDuration(curve);
        y = self.getYTM(self.getBondPrice(curve))
        return MacDuration / (1+y/self.feq)

    def getDV01(self, curve):
        
        ModDuration = self.getModDuration(curve)
        bondPrice   = self.getBondPrice(curve)
        return ModDuration * bondPrice  / self.face;
            
    def getYTM(self,bondPrice):
        error_function = lambda y: abs(bondPrice - self.getBondPrice_usingYTM(y));
        result = op.fmin(error_function,[0.05], disp = 0);
        return result[0];
        