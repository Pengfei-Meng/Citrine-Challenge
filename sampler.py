#!/usr/bin/env python
import sys, copy, math, random, pdb, time
from collections import deque
from constraints import Constraint

import numpy as np

from scipy import optimize


class Solution():

    def __init__(self, fname):

        
        self.con = Constraint(fname)
        self.num_x = self.con.n_dim

        self.outfile = 'output_' + fname
        with open(self.outfile, 'w') as f:    
            f.write(" ".join(map(str, self.con.example))) 
            f.write("\n") 

        self.ineq_cons = {'type': 'ineq',
             'fun' : lambda x: self.con.eval_con(x.tolist())}

        bound = [0.0, 1.0]
        self.bounds = np.asarray([bound]*self.num_x)


    def solve(self, n_results=100):
        
        x0_all = np.random.random_sample((n_results*2, self.num_x))

        cnt = 0
        for i in range(len(x0_all)):
            x0 = x0_all[i, :]
            # print 'Initial: ', x0

            if self.con.apply(x0.tolist()):
                x_feasible = x0
            else:
                try: 
                    x_feasible = self.optimize_feasible(x0)
                except:
                    continue
            
            with open(self.outfile, 'a') as f: 
                f.write(" ".join(map(str, x_feasible))) 
                f.write("\n") 

            cnt += 1
            if cnt == n_results:
                break
                            

    def optimize_feasible(self, x0):
        res = optimize.minimize(self.f, x0, method='SLSQP', 
                       constraints=[self.ineq_cons], options={'ftol': 1e-8, 'disp': False},
                       bounds=self.bounds)
        # print 'Optimal: ', res.x
        return res.x

    def f(self, x):
        constr = self.con.eval_con(x.tolist())
        constr[np.where(constr>0)] = 0
        return np.sum(np.square(constr))

    def constraint(self, x):
        constr = self.con.eval_con(x.tolist())
        return constr



if __name__ == "__main__":
        
    # fname = 'mixture.txt'
    # fname = 'example.txt'
    # fname = 'formulation.txt'
    fname = 'alloy.txt'
    # fname = sys.argv[1]

    start = time.time()

    sol_obj = Solution(fname) 
    sol_obj.solve(1000)

    end = time.time()
    duration = end-start

    
    # with open(sol_obj.outfile , 'a') as f:
    #     f.write("==================\n") 
    #     f.write("Elapsed time in seconds: " + "%s\n" % duration) 

    print 'Completed.'


