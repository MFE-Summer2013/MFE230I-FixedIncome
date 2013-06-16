'''
Created on Jun 15, 2013

@author: Billy
'''

from math import *

def rates(DF, T, feq = -1):
    spotRates = []
    if feq == -1:
        for df, t in zip(DF, T):
            spotRates.append(log(1.0/df) / t)
    else:
        for df, t in zip(DF, T):
            spotRates.append((pow(1/df, 1/t/feq) - 1) * feq)
    return spotRates

def getDF(rates, T, feq=-1):
    DF = []
    if feq == -1:
        for r, t in zip(rates,T):
            DF.append(exp(-r*t))
    else:
        for r, t in zip(rates,T):
            DF.append(pow(1+r/feq, -feq*t));
    return DF


def getFowardRates(DF, T, feq = -1):
    forwardRates = []
    if feq == -1:
        forwardRates.append(log(1/DF[0]) / T[0])
        for i in range(len(DF)-1):
            dt = T[i+1] - T[i]
            forwardRates.append(log(DF[i]/DF[i+1]) / dt)
    else:
        forwardRates.append((pow(1/DF[0], 1/T[0]/feq) - 1) * feq)
        for i in range(len(DF)-1):
            dt = T[i+1] - T[i]
            forwardRates.append( (pow(DF[i]/DF[i+1], 1/dt/feq) -1) * feq)
    return forwardRates

def interpolate(rates, T, newT):
    #make sure T and newT are sorted
    start_t = 0
    T_length = len(T)
    newRates = []
    new_T = []
    for new_t in newT:
        for i in range(start_t, T_length):
            if new_t == T[i]:
                newRates.append(rates[i])
                new_T.append(new_t)
                break
            elif new_t < T[i]:
                if i + 1 < T_length and i != 0:
                    dt = T[i] - T[i-1]
                    newRates.append((T[i] - new_t)/dt * rates[i-1] + (new_t - T[i-1])/dt * rates[i]);
                    new_T.append(new_t)
                start_t = i
                break
        if start_t == 0:
            continue
        if start_t == T_length:
            break
    return newRates, new_T

def parYield (DF, T, feq):
    t = 0.5
    newT = []
    while(t < T[-1]):
        newT.append(t)
        t += 0.5;
        
    spotRates = rates(DF,T,feq);
    newRates, newT = interpolate(spotRates, T, newT); 
    newDF = getDF(newRates, newT, feq);
    parYield = []
    sumDF = 0
    for df in newDF:
        sumDF += df
        parYield. append(2*(1 - df ) / sumDF);
    return parYield, newT
    
    
def parYield_forward (start_t, DF, T, feq):
    
    t = start_t
    newT = []
    while(t < T[-1]):
        newT.append(t)
        t += 0.5;
        
    spotRates = rates(DF,T,feq);
    newRates, newT = interpolate(spotRates, T, newT); 
    newDF = getDF(newRates, newT, feq);
    
    parYield = []
    sumFDF = 0
    for i in range(1,len(newDF)):
        FDF = newDF[i] / newDF[0]
        sumFDF += FDF
        parYield. append(2*(1 - FDF ) / sumFDF);
    newT.pop(0)
    return parYield, newT
    
    