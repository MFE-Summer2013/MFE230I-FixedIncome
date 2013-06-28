'''
Created on Jun 21, 2013

@author: Billy
'''

import yieldCurve as yc
import readData
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import Bond

if __name__ == '__main__':
    pass

#Setting Fond of Curve
font = {'family' : 'Arial'}
matplotlib.rc('font', **font)

## READ DATA FROM THE FILE
T, DF = readData.readFile('HW1_data.csv',1)

#FIT POLYNOMIAL MODEL
from IR_Models import Polynomial
poly_model = Polynomial.Polynomial()
poly_model.estimate(DF, T)

## SET YILED CURVE
T = np.arange(0.5, 31, 0.5)
DF = poly_model.fit(T)
fitCurve = yc.YieldCurve()
fitCurve.setCurve(T, DF)

# GET THE PARYIELD
T_par, parYield = fitCurve.getParYield();

MacDuration = []
ModDuration = []
DV01 = []

for t, py in zip(T_par, parYield):
    myBond = Bond.Bond(100, py, t)
    MacDuration.append(myBond.getMacDuration(fitCurve))
    ModDuration.append(myBond.getModDuration(fitCurve))
    DV01.append(myBond.getDV01(fitCurve))
plt.figure(1)    
plt.subplot(1,2,1)
plt.plot(T_par,MacDuration, label="Mac Duration")
plt.plot(T_par,ModDuration, label="Mod Duration")
plt.ylabel('Duration (years)')
plt.xlabel('Time to Maturity')
plt.legend(loc = 4,prop={'size':10})

plt.subplot(1,2,2)
plt.plot(T_par,DV01, label = "DV01")
plt.ylabel('DV01')
plt.xlabel('Time to Maturity')

# QUESTION 2

MacDuration2 = []
ModDuration2 = []
MacDuration12 = []
ModDuration12 = []

for t in T_par:
    myBond2 = Bond.Bond(100, 0.02, t)
    myBond12 = Bond.Bond(100,12, t)
    
    MacDuration2.append(myBond2.getMacDuration(fitCurve))
    ModDuration2.append(myBond2.getModDuration(fitCurve))
    
    MacDuration12.append(myBond12.getMacDuration(fitCurve))
    ModDuration12.append(myBond12.getModDuration(fitCurve))

plt.figure(3)
plt.plot(T_par,MacDuration2,'b', label="Mac Duration 2%")
plt.plot(T_par,ModDuration2,'b--', label="Mod Duration 2%")
plt.plot(T_par,MacDuration12,'g', label="Mac Duration 12%")
plt.plot(T_par,ModDuration12,'g--', label="Mod Duration 12%")
plt.legend(loc = 4,prop={'size':10})
plt.ylabel('Duration (Years)')
plt.xlabel('Time to Maturity')

# QUESTION 3
modDuration_10Y_par = ModDuration[10*2-1];
modDuration_05Y_par = ModDuration[5*2-1];
modDuration_15Y_par = ModDuration[15*2-1];
print "=== QUESTION 3 === \n"
print "Duration (Mod) of 10 Year Bond:     %f"%(modDuration_10Y_par)
print "Duration (Mod) of 5  Year Bond:     %f"%(modDuration_05Y_par)
print "Duration (Mod) of 15  Year Bond:    %f"%(modDuration_15Y_par)
print "Position of 5 Year Bond:            %f"%(-(modDuration_10Y_par / modDuration_05Y_par) * 100)
print "Position of 15 Year Bond:           %f"%(-(modDuration_10Y_par / modDuration_15Y_par) * 100)

# QUESTION 4

computeMatrix = np.asmatrix([[modDuration_05Y_par, modDuration_15Y_par], [1,1]]);
targetMatrix = np.asmatrix([[-modDuration_10Y_par], [-1]])
print "====QUESTION 4 ===\n"
weights = np.linalg.inv(computeMatrix) * targetMatrix;
print "The Weights of the 5 and 15-y bonds are "
print weights

# QUESTION 56
print "\n===QUESTION 5+6 ==="
bond1y = Bond.Bond(100,0,1)
bond3y = Bond.Bond(100,0,3)
bond7y = Bond.Bond(100,0,7)

print "Year, \t Mac Dura. \t Mod Dura"
print "%d \t %f \t %f"%(1,bond1y.getMacDuration(fitCurve), bond1y.getModDuration(fitCurve))
print "%d \t %f \t %f"%(3,bond3y.getMacDuration(fitCurve), bond3y.getModDuration(fitCurve))
print "%d \t %f \t %f"%(7,bond7y.getMacDuration(fitCurve), bond7y.getModDuration(fitCurve))

# QUESTION 7
print "\n===QUESTION 7 ===\n"

spotRates       = fitCurve.getSpotRates(2);

upward_10bp     = np.asarray(spotRates) + 10.0/10000
upward_300bp    = np.asarray(spotRates) + 300.0/10000
downward_10bp   = np.asarray(spotRates) - 10.0/10000
downward_300bp  = np.asarray(spotRates) - 300.0/10000

DF_upward_10bp = yc.spotRates_to_DF(upward_10bp, T, 2)
DF_upward_300bp = yc.spotRates_to_DF(upward_300bp, T, 2)
DF_downward_10bp = yc.spotRates_to_DF(downward_10bp, T, 2)
DF_downward_300bp = yc.spotRates_to_DF(downward_300bp, T, 2)

curve_upward_10bp = yc.YieldCurve();
curve_upward_300bp = yc.YieldCurve();
curve_downward_10bp = yc.YieldCurve();
curve_downward_300bp = yc.YieldCurve();

curve_upward_10bp.setCurve(T, DF_upward_10bp)
curve_upward_300bp.setCurve(T, DF_upward_300bp)
curve_downward_10bp.setCurve(T, DF_downward_10bp)
curve_downward_300bp.setCurve(T, DF_downward_300bp)

approxChange_u10bp = []
approxChange_u300bp = []
approxChange_d10bp = []
approxChange_d300bp = []

exactChange_u10bp = []
exactChange_u300bp = []
exactChange_d10bp = []
exactChange_d300bp = []

for t, py in zip(T_par, parYield):
    
    parBond = Bond.Bond(100,py,t)
    modDuration = parBond.getModDuration(fitCurve)
    
    approxChange_u10bp.append( - modDuration * 100 * 10/10000)
    approxChange_d10bp.append( + modDuration * 100 * 10/10000)
    approxChange_u300bp.append( - modDuration * 100 * 300/10000)
    approxChange_d300bp.append( + modDuration * 100 * 300/10000)
    
    exactChange_u10bp.append(parBond.getBondPrice(curve_upward_10bp) - 100)
    exactChange_u300bp.append(parBond.getBondPrice(curve_upward_300bp) - 100)
    exactChange_d10bp.append(parBond.getBondPrice(curve_downward_10bp) - 100)
    exactChange_d300bp.append(parBond.getBondPrice(curve_downward_300bp) - 100)

plt.figure(4)

plt.subplot(2,2,1)
plt.plot(T_par, approxChange_u10bp,  label='approx u10p')
plt.plot(T_par, exactChange_u10bp,  label='exact u10p')
plt.legend(loc = 1,prop={'size':10})
plt.ylabel("Change in Price")
plt.xlabel("Time to Maturity")

plt.subplot(2,2,2)
plt.plot(T_par, approxChange_u300bp, label='approx u300p')
plt.plot(T_par, exactChange_u300bp, label='exact u300p')
plt.legend(loc = 1,prop={'size':10})
plt.ylabel("Change in Price")
plt.xlabel("Time to Maturity")

plt.subplot(2,2,3)
plt.plot(T_par, approxChange_d10bp,  label='approx d10p')
plt.plot(T_par, exactChange_d10bp,  label='exact d10p')
plt.legend(loc = 4,prop={'size':10})
plt.ylabel("Change in Price")
plt.xlabel("Time to Maturity")

plt.subplot(2,2,4)
plt.plot(T_par, approxChange_d300bp, label='approx d300p')
plt.plot(T_par, exactChange_d300bp, label='exact d300p')
plt.legend(loc = 4,prop={'size':10})
plt.ylabel("Change in Price")
plt.xlabel("Time to Maturity")

plt.show()