'''
Created on Jun 15, 2013

@author: Billy
'''

from scipy import optimize as op
import math
import LossFunctions

class NelsonSiegel(object):
    '''
    Modeling the Nelson Siegel Interest Rate Models
    '''
    def __init__(self, param):
        '''
        Constructor
        '''
        self.param = param
        
    def estimateCurve(self, init_param, data):
        result = op.fmin(LossFunctions.NS_error, init_param, data);
        self.param = result.tolist();
        
    def getYield(self, T):
        y = []
        for t in T:
            short_end = ((1-math.exp(-t*self.param[3])) / (t*self.param[3])) * self.param[1]
            hump      = ((1-math.exp(-t*self.param[4])) / (t*self.param[4]) - math.exp(-t*self.param[4])) * self.param[2]
            y.append( self.param[0] +  short_end + hump)  
        return y
    