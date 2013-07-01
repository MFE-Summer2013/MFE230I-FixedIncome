'''
Created on Jun 30, 2013

@author: Billy
'''

import numpy as np
from IR_Models import Simple_LeeHo
import sys
import copy

class Mortgage(object):
    '''
    classdocs
    '''
    

    def __init__(self, initvalue, mRate, T, feq):
        '''
        Constructor
        '''
        
        self.face = initvalue
        self.r = mRate
        self.T = T
        self.feq = feq
        
        r = self.r / feq
        
        factor = 1 / r * ( 1 - np.power(1+r, - feq*T))
        self.pmt =  initvalue / factor
        
    def tree_withoutPrepayment(self, model, display = False):
        
        if len(model.tree) != self.T * self.feq:
            print "Periods does not match"
            return
        
        valueTree = []
        
        for i in range(self.T * self.feq-1,-1,-1):
            
            value = []
            
            rates = model.tree[i]
            
            for j in range(i+1):
                if i == self.T * self.feq-1:
                    value.append(self.pmt / (1+rates[j]))
                else:
                    prevalue = valueTree[-1]
                    value.append((self.pmt + prevalue[j] * 0.5 + prevalue[j+1] * 0.5)/(1+rates[j]))
            valueTree.append(value)
        
    
        valueTree.reverse()
        
        
        if display:        
            self.printTable(valueTree, "MORTGAGE WITHOUT PREPAYMENT")
            
        return valueTree
    
    def optionPayoff(self, model, display = False):
        
        schedule = self.paymentSchedule()
        optTree = copy.deepcopy(self.tree_withoutPrepayment(model))
        
        for i, opt in enumerate(optTree):
            for j in range(len(opt)):
                opt[j] = max(0.0, opt[j] - schedule[i][2])

        if display:
            self.printTable(optTree, "OPTION PAYOFF")
            
        return optTree
            
    def optionvalue(self, model, display = False):
        
        optValue = []
        optExe   = []
        
        optPayoff = self.optionPayoff(model)
        tree = model.tree
            
        optValue.append(optPayoff[-1])
        currentExe = []
        for rate in optPayoff[-1]:
            if rate > 0:
                currentExe.append(True)
            else:
                currentExe.append(False)
        
        optExe.append(currentExe)
        
        for i in range(len(tree)-2,-1,-1):
            
            currentValue = []
            currentExe   = []
            for j in range(i+1):
                discountValue = (0.5*optValue[-1][j] + 0.5*optValue[-1][j+1])/ (1+tree[i][j])
                
                if optPayoff[i][j] > discountValue:
                    currentValue.append(optPayoff[i][j])
                    currentExe.append(True)
                else:
                    currentValue.append(discountValue)
                    currentExe.append(False)
            optValue.append(currentValue)
            optExe.append(currentExe)
            
        optValue.reverse()
        optExe.reverse()
        
        if display:
            self.printTable(optValue, "OPTION VALUE")
            self.printTable(optExe, "EXERCISE")
        
        return optValue, optExe
        
    def prin_and_int_pathThrough(self, model, display):
    
        optValue, optExe = self.optionvalue(model)
        schedule = self.paymentSchedule()
        tree = model.tree
        
        ## initialize
        PO = []
        IO = []
        
        curPO = []
        curIO = []
        for i in range(len(optValue)):
            if optExe[-1][i]:
                curPO.append(schedule[-2][2])
                curIO.append(0)
            else:
                curPO.append(schedule[-1][1] / (1+tree[-1][i]))
                curIO.append(schedule[-1][0] / (1+tree[-1][i]))
        
        PO.append(curPO)
        IO.append(curIO)
        
        for i in range(len(optValue)-2,-1,-1):
            curPO = []
            curIO = []
            for j in range(i+1):
                if optExe[i][j]:
                    curPO.append(schedule[i][2])
                    curIO.append(0)
                else:
                    POvalue = (0.5*PO[-1][j] + 0.5*PO[-1][j+1] + schedule[i+1][1]) / (1+tree[i][j])
                    IOvalue = (0.5*IO[-1][j] + 0.5*IO[-1][j+1] + schedule[i+1][0]) / (1+tree[i][j])
                    curPO.append(POvalue)
                    curIO.append(IOvalue)
                    
            PO.append(curPO)
            IO.append(curIO)
    
        PO.reverse()
        IO.reverse()
        
        if display:
            self.printTable(PO, "PO VALUE")
            self.printTable(IO, "IO VALUE")
    def paymentSchedule(self, display = False):
        
        schedule = [(0,0,100)] #IRPAYMENT, PRINCiPAL, OUTSTANDING
        
        for i in range(self.feq*self.T):
            IR = schedule[-1][2] * self.r / self.feq
            Principal = self.pmt - IR
            outStanding = schedule[-1][2] - Principal
            schedule.append((IR,Principal, outStanding))
        
        if display:
            print "Payment Schedule, RATES / PRINCIPAL / OUTSTANDING"
            for i in range(self.feq * self.T + 1):
                sys.stdout.write('%d\t\t'%(i))
            sys.stdout.write("\n")
            for i in range(3):
                for tuple in schedule:
                    sys.stdout.write('%f\t'%(tuple[i]))
                sys.stdout.write("\n")
            print ''
        return schedule
    
    def printTable(self,tree, name):
        
        print name
        treeSize = len(tree)
        for i in range(treeSize):
            sys.stdout.write("%g\t\t"%(i))
        sys.stdout.write("\n")
        for j in range(treeSize):
            for i in range(j):
                sys.stdout.write("\t\t")
            for i in range(j,treeSize):
                sys.stdout.write("%f\t"%(tree[i][j]))
            sys.stdout.write("\n")
        print ""
        
        