'''
Created on Jun 18, 2013

@author: Billy
'''

def readFile (fileName,nl_skip=0):
    
    with open(fileName,'rb') as file:
        lines=[line.strip().split(',') for line in file.readlines()[nl_skip:]]
        T,DF=zip(*lines)
    
    return T,DF