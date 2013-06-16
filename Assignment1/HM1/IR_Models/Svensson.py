'''
Created on Jun 15, 2013

@author: Billy
'''

from scipy import optimize as op
import math
import LossFunctions


class Svensson(object):
    '''
    classdocs
    '''

    def __init__(self, param):
        '''
        Constructor
        '''
        self.param = param
        
    def estimateCurve(self, init_param, data):
        result = op.fmin(LossFunctions.Svensson_error, init_param, data);
        self.param = result.tolist();
        
    def getYield(self, T):
        y = []
        for t in T:
            short_end = ((1-math.exp(-t*self.param[4])) / (t*self.param[4])) * self.param[1]
            hump1     = ((1-math.exp(-t*self.param[4])) / (t*self.param[4]) - math.exp(-t*self.param[4])) * self.param[2]
            hump2     = ((1-math.exp(-t*self.param[5])) / (t*self.param[5]) - math.exp(-t*self.param[5])) * self.param[3]
            y.append(self.param[0] + short_end + hump1 + hump2)      
        return y
    