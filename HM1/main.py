'''
Created on Jun 18, 2013

@author: Billy
'''

import numpy as nm

if __name__ == '__main__':
    pass

print 'Testing packages'

a = [2,3,4,5,6,7];
a = nm.asarray(a)
print a[2:5] - a[1:4];
print a * a;

a = [1,4,5,9,10]
b = [0,4,8,12]

g = lambda x : x**2
print g(8)

f = lambda a