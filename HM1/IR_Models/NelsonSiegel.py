'''
Created on Jun 18, 2013

@author: Billy
'''

import numpy as np
from scipy import optimize
import yieldCurve as ys


class NelsonSiegel(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        # parameter: beta1, beta2, beta3, lambda2, lambda3
        self.param = [0,0,0,0,0]
    
    def estimate(self, init, DF,T, durationWeighting = False):
        result = optimize.fmin(NS_error, init, (T,DF,durationWeighting))
        self.param = result.tolist()

    def fit(self, T):
        T = np.asarray(T)
        short_end = ((1-np.exp(-T*self.param[3])) / (T*self.param[3])) * self.param[1]
        hump      = ((1-np.exp(-T*self.param[4])) / (T*self.param[4]) - np.exp(-T*self.param[4])) * self.param[2]
        fitted_y  = self.param[0] +  short_end + hump
        return fitted_y
    
    def getEstError(self, DF, T, durationWeighting = False):
        return NS_error(self.param, DF, T, durationWeighting)

def NS_error(param, *data):
    #param beta_1, beta_2, beta_3, lambda2, lambda3
    T = np.asarray(data[0])
    DF = np.asarray(data[1])
    d_weight = data[2]
    
    if d_weight:
        I_w = 1;
    else:
        I_w = 0
        
    short_end = ((1-np.exp(-T*param[3])) / (T*param[3])) * param[1]
    hump      = ((1-np.exp(-T*param[4])) / (T*param[4]) - np.exp(-T*param[4])) * param[2]
    fitted_y  = param[0] +  short_end + hump
    fitted_DF = ys.spotRates_to_DF(fitted_y, T)
    
    weights = 1 + (T-1) * I_w;
    
    error2 = np.power(fitted_DF - DF, 2) * weights
    return sum(error2);
    
    