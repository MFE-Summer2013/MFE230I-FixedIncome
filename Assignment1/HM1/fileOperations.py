'''
Created on Jun 15, 2013

@author: Billy
'''

import csv

def getFile(dataFileName):
    T = [];
    DF = [];
    with open(dataFileName, 'rb') as dataFile:
        reader = csv.reader(dataFile);
        next(reader,None)
        for line in reader:
            discount = float(line[1]) / 100.0;
            T.append(float(line[0]));
            DF.append(discount);
    return T, DF