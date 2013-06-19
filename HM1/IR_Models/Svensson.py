'''
Created on Jun 18, 2013

@author: Billy
'''

import numpy as np
from scipy import optimize
import yieldCurve as ys


class Svensson(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        # parameter: beta1, beta2, beta3, beta4, lambda2, lambda3
        self.param = [0,0,0,0,0,0]
    
    def estimate(self, init, DF,T, durationWeighting = False):
        result = optimize.fmin(SV_error, init, args=(T,DF,durationWeighting),maxfun=10000)
        self.param = result.tolist()

    def fit(self, T):
        T = np.asarray(T)
        short_end = ((1-np.exp(-T*self.param[4])) / (T*self.param[4])) * self.param[1]
        hump1     = ((1-np.exp(-T*self.param[4])) / (T*self.param[4]) - np.exp(-T*self.param[4])) * self.param[2]
        hump2     = ((1-np.exp(-T*self.param[5])) / (T*self.param[5]) - np.exp(-T*self.param[5])) * self.param[3]
        fitted_y  = self.param[0] +  short_end + hump1 + hump2
        return fitted_y
    
    def getEstError(self, DF, T, durationWeighting = False):
        return SV_error(self.param, T, DF, durationWeighting)

def SV_error(param, *data):
    #param beta_1, beta_2, beta_3, lambda2, lambda3
    T = np.asarray(data[0])
    DF = np.asarray(data[1])
    d_weight = data[2]
    
    if d_weight:
        I_w = 1;
    else:
        I_w = 0
        
    short_end = ((1-np.exp(-T*param[4])) / (T*param[4])) * param[1]
    hump1     = ((1-np.exp(-T*param[4])) / (T*param[4]) - np.exp(-T*param[4])) * param[2]
    hump2     = ((1-np.exp(-T*param[5])) / (T*param[5]) - np.exp(-T*param[5])) * param[3]
    fitted_y  = param[0] +  short_end + hump1 + hump2
    fitted_DF = ys.spotRates_to_DF(fitted_y, T)
    
    weights = 1 + (1/T-1) * I_w;
    
    error2 = np.power(fitted_DF - DF, 2) * weights
    return sum(error2);
    
    