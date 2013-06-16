'''
Created on Jun 15, 2013

@author: Billy
'''

import math

def NS_error(param, *data):
    #param beta_1, beta_2, beta_3, lambda2, lambda3
    error2 = 0;
    for i,T in enumerate(data[0]):
        
        short_end = ((1-math.exp(-T*param[3])) / (T*param[3])) * param[1]
        hump      = ((1-math.exp(-T*param[4])) / (T*param[4]) - math.exp(-T*param[4])) * param[2]
        fitted_y  = param[0] +  short_end + hump      
        error2 += (fitted_y  - data[1][i])**2;
        
    return error2;

def Svensson_error(param, *data):
    #param beta_1, beta_2, beta_3, beta_4, lambda2, lambda3
    error2 = 0;
    for i,T in enumerate(data[0]):
        short_end = ((1-math.exp(-T*param[4])) / (T*param[4])) * param[1]
        hump1     = ((1-math.exp(-T*param[4])) / (T*param[4]) - math.exp(-T*param[4])) * param[2]
        hump2     = ((1-math.exp(-T*param[5])) / (T*param[5]) - math.exp(-T*param[5])) * param[3]
        fitted_y  = param[0] +  short_end + hump1 + hump2      
        error2 += (fitted_y  - data[1][i])**2;
    return error2;