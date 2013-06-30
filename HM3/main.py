'''
Created on Jun 28, 2013

@author: Billy
'''
import yieldCurve as yc
import readData
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import Bond
import pandas as pd

if __name__ == '__main__':
    pass

#Setting Fond of Curve
font = {'family' : 'Arial'}
matplotlib.rc('font', **font)
'''

## QUESTION 1
## READ DATA FROM THE FILE
T, DF = readData.readFile('HW1_data.csv',1)

#FIT POLYNOMIAL MODEL
from IR_Models import Polynomial
poly_model = Polynomial.Polynomial()
poly_model.estimate(DF, T)

## SET YILED CURVE
T = np.arange(0.5, 30.5, 0.5)
DF = poly_model.fit(T)
fitCurve = yc.YieldCurve()
fitCurve.setCurve(T, DF)

# GET THE PARYIELD
T_par, parYield = fitCurve.getParYield();
convex = []
for t, py in zip(T_par, parYield):
    parBond = Bond.Bond(100, py, t)
    convex.append(parBond.getConvexity(fitCurve))

plt.figure(1)
plt.plot(T_par, convex, '-o')
plt.ylabel('Convexity')
plt.xlabel('Time to Maturity of Par Bond')

## QUESTION 2
plt.figure(2)
currentRates = fitCurve.getSpotRates(2);
shift = [10.0/10000, -10.0/10000, 300.0/10000, -300.0/10000];
for i,s in enumerate(shift):
    shiftedRates = np.asarray(currentRates) + s
    shiftedDF    = yc.spotRates_to_DF(shiftedRates, T,2)
    shiftedCurve = yc.YieldCurve()
    shiftedCurve.setCurve(T, shiftedDF)
    
    
    approxChange = []
    approxChangeD = []
    exactChange  = []
    for t, py in zip(T_par, parYield):
        parBond = Bond.Bond(100,py,t)
        ModDuration = parBond.getModDuration(fitCurve)
        Convexity   = parBond.getConvexity(fitCurve)
        BondPrice   = parBond.getBondPrice(shiftedCurve)
        
        approxChange.append( - ModDuration * s * 100 + 0.5 * Convexity * s * s*100)
        approxChangeD.append( - ModDuration * s * 100)
        exactChange.append(BondPrice - 100)
    
    plt.subplot(2,2,i+1)
    plt.plot(T_par,approxChange, '-', label='Approx D+C');
    plt.plot(T_par,approxChangeD, '-', label='Approx D');
    plt.plot(T_par,exactChange, '-', label='Exact')
    plt.title("Shifts = %g bps"%(s*10000))
    plt.legend(loc = 4,prop={'size':10})
    
'''
## QUESTION 3
import datetime as dt
fileName = "termstruc.csv"
startDate = dt.datetime(1986,1,1)
endDate   = dt.datetime(2008,12,31)

rawData = pd.read_csv(fileName);
rawData['Date'] = pd.to_datetime(rawData['Date'])
rawData = rawData[(rawData['Date'] >= startDate) & (rawData['Date'] <= endDate)]
'''
sortedDate = rawData.sort(['1'])
minData = sortedDate[0:1]
maxData = sortedDate[-1:]

print ' ======== QUESTION 3 ==============\n'

print "PART(a)"
print "Min one-year rates: ", minData.iloc[0,1], ' on ', dt.datetime.strftime(minData.iloc[0,0], '%Y-%m-%d');
print "Max one-year rates: ", maxData.iloc[0,1], ' on ', dt.datetime.strftime(maxData.iloc[0,0], '%Y-%m-%d');

minCurve = yc.YieldCurve();
maxCurve = yc.YieldCurve();

T = np.arange(1,31,1)

ratesMin = np.asarray(minData.iloc[:,1:])[0] / 100
ratesMax = np.asarray(maxData.iloc[:,1:])[0] / 100
DFMin = yc.spotRates_to_DF(ratesMin, T)
DFMax = yc.spotRates_to_DF(ratesMax, T)

minCurve.setCurve(T, DFMin)
maxCurve.setCurve(T, DFMax)

plt.figure(3)
plt.subplot(1,2,1)
plt.plot(T,ratesMin, label='Spot Rates')
plt.title('Min Curve at ' + dt.datetime.strftime(minData.iloc[0,0], '%Y-%m-%d'))
minFowardRates = minCurve.getForwardRates_PeriodByPeriod()
plt.plot(T,minFowardRates, label='Forward Rates')
plt.ylabel('Spot / Forward Rates')
plt.xlabel('T')
plt.legend(loc = 1,prop={'size':10})


plt.subplot(1,2,2)
plt.plot(T,ratesMax, label='Spot Rates')
plt.title('Max Curve at ' + dt.datetime.strftime(maxData.iloc[0,0], '%Y-%m-%d'))
maxFowardRates = maxCurve.getForwardRates_PeriodByPeriod()
plt.plot(T,maxFowardRates, label='Forward Rates')
plt.ylabel('Spot / Forward Rates')
plt.xlabel('T')
plt.legend(loc = 1,prop={'size':10})

##################################################################
print "\n"
print "PART(b)"

slope = rawData['10'] - rawData['1']
slope.sort()

minIndex = slope.first_valid_index()
maxIndex = slope.last_valid_index()

minDate  = rawData.loc[minIndex,'Date']
maxDate  = rawData.loc[maxIndex,'Date']

ratesMin = np.asarray(rawData.loc[minIndex].iloc[1:]) / 100
ratesMax = np.asarray(rawData.loc[maxIndex].iloc[1:]) / 100

DFMin = yc.spotRates_to_DF(ratesMin, T)
DFMax = yc.spotRates_to_DF(ratesMax, T)

minCurve.setCurve(T, DFMin)
maxCurve.setCurve(T, DFMax)

plt.figure(4)
plt.subplot(1,2,1)
plt.plot(T,ratesMin, label='Spot Rates')
plt.title('Min Slope Curve at ' + dt.datetime.strftime(minDate, '%Y-%m-%d'))
minFowardRates = minCurve.getForwardRates_PeriodByPeriod()
plt.plot(T,minFowardRates, label='Forward Rates')
plt.ylabel('Spot / Forward Rates')
plt.xlabel('T')
plt.legend(loc = 1,prop={'size':10})


plt.subplot(1,2,2)
plt.plot(T,ratesMax, label='Spot Rates')
plt.title('Max Slope Curve at ' + dt.datetime.strftime(maxDate, '%Y-%m-%d'))
maxFowardRates = maxCurve.getForwardRates_PeriodByPeriod()
plt.plot(T,maxFowardRates, label='Forward Rates')
plt.ylabel('Spot / Forward Rates')
plt.xlabel('T')
plt.legend(loc = 1,prop={'size':10})


##################################################################
print "\n"
print "PART(c)"

conv = 2*rawData['15'] - rawData['1'] - rawData['30']
conv.sort()

minIndex = conv.first_valid_index()
maxIndex = conv.last_valid_index()

minDate  = rawData.loc[minIndex,'Date']
maxDate  = rawData.loc[maxIndex,'Date']

ratesMin = np.asarray(rawData.loc[minIndex].iloc[1:]) / 100
ratesMax = np.asarray(rawData.loc[maxIndex].iloc[1:]) / 100

DFMin = yc.spotRates_to_DF(ratesMin, T)
DFMax = yc.spotRates_to_DF(ratesMax, T)

minCurve.setCurve(T, DFMin)
maxCurve.setCurve(T, DFMax)

plt.figure(5)
plt.subplot(1,2,1)
plt.plot(T,ratesMin, label='Spot Rates')
plt.title('Min Covex Curve at ' + dt.datetime.strftime(minDate, '%Y-%m-%d'))
minFowardRates = minCurve.getForwardRates_PeriodByPeriod()
plt.plot(T,minFowardRates, label='Forward Rates')
plt.ylabel('Spot / Forward Rates')
plt.xlabel('T')
plt.legend(loc = 1,prop={'size':10})

plt.subplot(1,2,2)
plt.plot(T,ratesMax, label='Spot Rates')
plt.title('Max Covex Curve at ' + dt.datetime.strftime(maxDate, '%Y-%m-%d'))
maxFowardRates = maxCurve.getForwardRates_PeriodByPeriod()
plt.plot(T,maxFowardRates, label='Forward Rates')
plt.ylabel('Spot / Forward Rates')
plt.xlabel('T')
plt.legend(loc = 1,prop={'size':10})

'''

## QUESTION 4

change = rawData.shift(1) - rawData
change = np.asmatrix(change.iloc[1:,1:]) / 100
oneYear = np.transpose(np.asarray(rawData.shift(1).iloc[1:, 1:2])/100)[0]
date   = rawData.shift(1).iloc[1:,0:1]


size = (change.shape)[0]

stdWindow = []
for i in range(size - 60):
    
    subData = change[i:i+60]
    subData2 = np.power(subData,2)
    sum_window  = subData.sum(axis=0)
    sum2_window = subData2.sum(axis=0)
    
    var = (sum2_window - np.power(sum_window,2) / 60)/ 59
    std = np.sqrt(var)
    stdWindow.append(np.asarray(std)[0])

stdWindow = np.asmatrix(stdWindow)

stdWindow = np.transpose(stdWindow)

index = [1, 3, 5, 10, 20, 30]
fig = plt.figure(6)
for i,t in enumerate(index):
    ax1 = fig.add_subplot(2,3,i+1)
    ax1.plot(stdWindow[t-1].tolist()[0], label = 'Std of %d-year rates change'%(t))
    plt.legend(loc = 4,prop={'size':10})
    ax2 = ax1.twinx()
    ax2.plot(oneYear,'r--', label='One Year Rate')
    ax1.set_xlim(ax1.get_xlim()[::-1]) 

print "\n========= QUESTION 5 =========\n"
print "Correlation Matrix"
changeData = np.transpose(change)
correlationMatrix =  np.corrcoef(changeData[[0, 2, 4, 9, 19, 29]])
print correlationMatrix




print "\n========= QUESTION 6 ==========\n"

correlationMatrix = np.corrcoef(changeData)
eigenvalue, eigenvector = np.linalg.eig(correlationMatrix)


'''
plt.figure(6)
plt.plot(index, eigenvector[:,0],label='First')
plt.plot(index, eigenvector[:,1],label='Second')
plt.plot(index, eigenvector[:,2],label='Third')
'''

plt.figure(7)
plt.plot(eigenvector[:,0],label='First')
plt.plot(eigenvector[:,1],label='Second')
plt.plot(eigenvector[:,2],label='Third')


print "\n ========== QUESTION 7 ==============\n"

T = np.arange(1,31,1)

forwardRates = []
for i in range(size+1):
    currentRates =  np.asarray(rawData.iloc[i:i+1,1:])[0] / 100
    DF           =  yc.spotRates_to_DF(currentRates, T)
    myCurve      =  yc.YieldCurve()
    myCurve.setCurve(T, DF)
    forwardRates.append(myCurve.getForwardRates_PeriodByPeriod())

forwardRates = pd.DataFrame(forwardRates)
changeForwardRates = forwardRates.shift(1) - forwardRates
changeForwardRates = np.asmatrix(changeForwardRates.iloc[1:, :])
oneYearForward = np.transpose(np.asarray(forwardRates.iloc[1:, 0:1]))[0]

print oneYearForward

STDEV = []
for i in range(size):
    currentBatch = changeForwardRates[i:i+60];
    STDEV.append(np.std(currentBatch,axis = 0))
    
STDEV = np.transpose(STDEV)

'''
for i in STDEV:
    print i 

index = [1, 3, 5, 10, 20, 30]
fig = plt.figure(8)
for i,t in enumerate(index):
    ax1 = fig.add_subplot(2,3,i+1)
    ax1.plot(STDEV[t-1].tolist()[0], label = 'Std of %d-year Forward rates change'%(t))
    plt.legend(loc = 4,prop={'size':10})
    ax2 = ax1.twinx()
    ax2.plot(oneYearForward,'r--', label='One Year Forward Rate')
    ax1.set_xlim(ax1.get_xlim()[::-1]) 
    '''

correlation = np.corrcoef(np.transpose(changeForwardRates))
eigenvalue, eigenvector = np.linalg.eig(correlation)
print eigenvector

plt.figure(9)
plt.plot(eigenvector[:,0],label='First')
plt.plot(eigenvector[:,1],label='Second')
plt.plot(eigenvector[:,2],label='Third')

plt.show()
