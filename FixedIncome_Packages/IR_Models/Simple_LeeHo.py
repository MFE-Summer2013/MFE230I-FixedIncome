'''
Created on Jun 29, 2013

@author: Billy
'''

import numpy as np
from scipy import optimize as op
import sys

class Simple_LeeHo(object):
    '''
    classdocs
    '''


    def __init__(self, vol):
        
        self.vol = vol
        
    def estimate(self, zeroRates):
        
        self.tree = [[zeroRates[0]]]
        self.m    = []
        
        numPeriods = len(zeroRates)
        
        for i in range(1, numPeriods):
            
            zeroPrice = 100 * np.power(1+zeroRates[i], -i-1)
            result = op.minimize(errorPrice, 0.010298, tol=1e-06, method='Nelder-Mead',args=(zeroPrice, i+1, self.tree, self.vol))
            m = result.x[0]
            self.m.append(m)
            lastRates = np.asarray(self.tree[-1])
            newRates = (lastRates + self.vol + m).tolist()
            newRates.append(lastRates[-1] - self.vol + m)
    
            self.tree.append(newRates)
    
    def print_tree(self):
        
        treeSize = len(self.tree)
        
        print "INTEREST RATE TREE"

        for i in range(treeSize):
            sys.stdout.write("%g\t\t"%(i))
        sys.stdout.write("\n")
        for j in range(treeSize):
            for i in range(j):
                sys.stdout.write("\t\t")
            for i in range(j,treeSize):
                sys.stdout.write("%f\t"%(self.tree[i][j]))
            sys.stdout.write("\n")
        print ""
        
        '''
        print "THE INTEREST RATE TREE:"
        size = len(self.tree)
        for i, rates in enumerate(self.tree):
            sys.stdout.write("%g\t"%(i))
            for j in range(size-i-1):
                    sys.stdout.write("\t")
            for rate in rates:
                sys.stdout.write("%f\t"%rate) 
            sys.stdout.write("\n")
        '''
            
def errorPrice(m, *data):
    
    m = m[0];
    
    targetBondPrice = data[0];
    nthPeriod = data[1]
    ratesTree = data[2]
    vol       = data[3]
    
    lastRates = np.asarray(ratesTree[-1])
    newRates = (lastRates + vol + m).tolist()
    newRates.append(lastRates[-1] - vol + m)
    bondPrice = 100 * np.ones(nthPeriod)
    
    for j in range(nthPeriod-1):
        bondPrice[j] = bondPrice[j] / (1+newRates[j]) * 0.5 + bondPrice[j+1] / (1+newRates[j+1]) * 0.5
    
    for i in range(nthPeriod-2, -1, -1):
        rates = ratesTree[i]
        for j in range(i):
            bondPrice[j] = bondPrice[j] / (1+rates[j]) * 0.5 + bondPrice[j+1] / (1+rates[j+1]) * 0.5
    
    price = bondPrice[0]/(1+ratesTree[0][0])

    return np.power(price - targetBondPrice,2)
    
