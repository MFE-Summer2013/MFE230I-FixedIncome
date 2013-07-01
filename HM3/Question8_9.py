'''
Created on Jun 29, 2013

@author: Billy
'''

if __name__ == '__main__':
    pass

import IR_Models.Simple_LeeHo as SHL

rates = [0.050, 0.055,0.057,0.059,0.06,0.061]

model = SHL.Simple_LeeHo(0.015)
model.estimate(rates)
model.print_tree()

from Product import Mortgage

mort = Mortgage.Mortgage(100,0.055,6,1)
mort.tree_withoutPrepayment(model, True)
mort.paymentSchedule(True)
mort.optionPayoff(model, True)
mort.optionvalue(model, True)
mort.prin_and_int_pathThrough(model, True)