'''
Created on Jun 18, 2013

@author: Billy
'''

import numpy as np

class Polynomial():

    def __init__(self):
        '''
        Constructor
        '''
    def estimate(self,DF,T):

        DF = np.asmatrix(DF)
        T = np.asmatrix(T)
        logDF = np.log(DF)
        
        XT = T
        for i in range(4):
            XT = np.vstack((XT,np.power(T,i+2)))

        XTX = XT*np.transpose(XT)
        self.param = np.linalg.inv(XTX) * XT * np.transpose(logDF)    

    def fit(self, T):

        XT = T
        for i in range(4):
            XT =  XT = np.vstack((XT,np.power(T,i+2)))
        logDF = np.transpose(XT) * self.param
        DF = np.exp(logDF)
        return np.array(DF).reshape(-1,).tolist()
        