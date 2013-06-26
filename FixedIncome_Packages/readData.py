'''
Created on Jun 18, 2013

@author: Billy
'''

import numpy as np

def readFile (fileName,nl_skip=0):
    with open(fileName,'rb') as f:
        lines=[line.strip().split(',') for line in f.readlines()[nl_skip:]]
    
    T,DF=zip(*lines)
    return np.array(T).astype(float).tolist(), (np.array(DF).astype(float)/100).tolist()
