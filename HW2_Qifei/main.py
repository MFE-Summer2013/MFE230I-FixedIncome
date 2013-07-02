'''
Created on Jun 24, 2013

@author: Qifei
'''

import numpy as np
from readData import readFile
from IR_Models import Polynomial
from yieldCurve import *
from Bond import Bond
import matplotlib.pyplot as plt

# Read data
T,DF = readFile('../../Assignment 1/Spreadsheet_for_problem_set_1.csv',1)
#T,DF = readFile('C:\Users\Qifei\Documents\Study\UCB\\2013 2.Summer\\230I-Fixed Income Markets\Assignments\Assignment 1\Spreadsheet_for_problem_set_1.csv')

# Get DFs using Polynomial fit
polynomial_model = Polynomial.Polynomial()
polynomial_model.estimate(DF, T)
T = np.arange(.5,31,.5)
DF = polynomial_model.fit(T)

# Get par yield
yc = YieldCurve()
yc.setCurve(T, DF)
par_yield = yc.getParYield()

# Question 1. Duration assuming semiannual bonds
Macaulay_D = np.zeros(30)
for i in range(1,31):
    Macaulay_D[i-1] = sum(T[:2*i] * par_yield[1][i*2-1]/2 * DF[:i*2]) + T[2*i-1]*DF[i*2-1]

Modified_D = Macaulay_D/(1+np.array(par_yield[1])[1:60:2])
DV01 = Modified_D / 100

Maturity = range(1,31)
plt.figure(1)
plt.subplot(1,2,1)
plt.plot(Maturity,Macaulay_D, label="Mac Duration")
plt.plot(Maturity,Modified_D, label="Mod Duration")
plt.ylabel('Duration (years)')
plt.xlabel('Time to Maturity')
plt.legend(loc = 4,prop={'size':10})

plt.subplot(1,2,2)
plt.plot(Maturity,DV01, label="DV01")
plt.ylabel('DV01')
plt.xlabel('Time to Maturity')
plt.legend(loc = 4,prop={'size':10})

# Question 2. 
Macaulay_D_2_pct = np.zeros(30)
for i in range(1,31):
    Macaulay_D_2_pct[i-1] = (sum(T[:2*i] * 0.02/2 * DF[:i*2]) + T[2*i-1]*DF[i*2-1]) / (sum(DF[:i*2]) * 0.02/2 + DF[i*2-1]) 

Macaulay_D_12_pct = np.zeros(30)
for i in range(1,31):
    Macaulay_D_12_pct[i-1] = (sum(T[:2*i] * 0.12/2 * DF[:i*2]) + T[2*i-1]*DF[i*2-1]) / (sum(DF[:i*2]) * 0.12/2 + DF[i*2-1])

plt.figure(2)
plt.plot(Maturity,Macaulay_D_2_pct, label="2% Mac Duration")
plt.plot(Maturity,Macaulay_D_12_pct, label="12% Mac Duration")
plt.ylabel('Duration (years)')
plt.xlabel('Time to Maturity')
plt.legend(loc = 4,prop={'size':10})

# Question 3
print Modified_D[9] * 100/100 / (Modified_D[4]/100)
print Modified_D[9] * 100/100 / (Modified_D[14]/100)

# Question 7
bp = .01/100

up_10 = np.zeros(30)
up_300 = np.zeros(30)
down_10 = np.zeros(30)
down_300 = np.zeros(30)
up_10_exact = np.zeros(30)
up_300_exact = np.zeros(30)
down_10_exact = np.zeros(30)
down_300_exact = np.zeros(30)

spotRates = yc.getSpotRates(2)
spotRates_up_10 = np.add(spotRates, 10*bp)
spotRates_up_300 = np.add(spotRates, 300*bp)
spotRates_down_10 = np.add(spotRates, -10*bp)
spotRates_down_300 = np.add(spotRates, -300*bp)

yc_up_10 = YieldCurve()
yc_up_10.setCurve(yc.T, spotRates_to_DF(spotRates_up_10, yc.T, 2))
yc_up_300 = YieldCurve()
yc_up_300.setCurve(yc.T, spotRates_to_DF(spotRates_up_300, yc.T, 2))
yc_down_10 = YieldCurve()
yc_down_10.setCurve(yc.T, spotRates_to_DF(spotRates_down_10, yc.T, 2))
yc_down_300 = YieldCurve()
yc_down_300.setCurve(yc.T, spotRates_to_DF(spotRates_down_300, yc.T, 2))

for i in range(30):
    up_10[i] = -Modified_D[i] * 10*bp * 100
    up_300[i] = -Modified_D[i] * 300*bp * 100
    down_10[i] = -Modified_D[i] * -10*bp * 100
    down_300[i] = -Modified_D[i] * -300*bp * 100
    
    up_10_exact[i] = Bond(100,par_yield[1][2*i+1], i+1).getBondPrice(yc_up_10) - 100;
    up_300_exact[i] = Bond(100,par_yield[1][2*i+1], i+1).getBondPrice(yc_up_300) - 100;
    down_10_exact[i] = Bond(100,par_yield[1][2*i+1], i+1).getBondPrice(yc_down_10) - 100;
    down_300_exact[i] = Bond(100,par_yield[1][2*i+1], i+1).getBondPrice(yc_down_300) - 100;

plt.figure(3)
plt.subplot(2,2,1)
plt.plot(Maturity,up_10, label="up 10bp Approximated")
plt.plot(Maturity,up_10_exact, label="up 10bp Exact")
plt.ylabel('Price Change ($)')
plt.xlabel('Time to Maturity')
plt.legend(loc = 3,prop={'size':10})

plt.subplot(2,2,2)
plt.plot(Maturity,up_300, label="up 300bp Approximated")
plt.plot(Maturity,up_300_exact, label="up 300bp Exact")
plt.ylabel('Price Change ($)')
plt.xlabel('Time to Maturity')
plt.legend(loc = 3,prop={'size':10})

plt.subplot(2,2,3)
plt.plot(Maturity,down_10, label="down 10bp Approximated")
plt.plot(Maturity,down_10_exact, label="down 10bp Exact")
plt.ylabel('Price Change ($)')
plt.xlabel('Time to Maturity')
plt.legend(loc = 4,prop={'size':10})

plt.subplot(2,2,4)
plt.plot(Maturity,down_300, label="down 300bp Approximated")
plt.plot(Maturity,down_300_exact, label="down 300bp Exact")
plt.ylabel('Price Change ($)')
plt.xlabel('Time to Maturity')
plt.legend(loc = 4,prop={'size':10})

plt.show()