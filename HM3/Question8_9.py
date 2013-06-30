'''
Created on Jun 29, 2013

@author: Billy
'''

if __name__ == '__main__':
    pass

import numpy as np
import IR_Models.Simple_LeeHo as SHL

rates = [0.050, 0.055,0.057,0.059,0.06,0.061]

model = SHL.Simple_LeeHo(0.015)
model.estimate(rates)
model.print_tree()

