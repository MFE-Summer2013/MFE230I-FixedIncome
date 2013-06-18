'''
Created on Jun 18, 2013

@author: Billy
'''

import csv

def readFile (fileName):
    T = []
    DF = []
    with open(fileName,'rb') as file:
        reader = csv.reader(file)
        reader.next()
        for line in reader:
            T.append(float(line[0]))
            DF.append(float(line[1])/100)
    return T, DF
