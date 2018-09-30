#!/usr/bin/python
import sys, copy, math, random, pdb, time
from collections import deque
from constraints import Constraint
import numpy as np
from scipy import optimize


class Solution():

    def __init__(self, fname, outfile, n_results):

        
        self.con = Constraint(fname)
        self.num_x = self.con.n_dim
        self.n_results = n_results

        self.outfile = outfile
        with open(self.outfile, 'w') as f:    
            f.write(" ".join(map(str, self.con.example))) 
            f.write("\n") 

        self.ineq_cons = {'type': 'ineq',
             'fun' : lambda x: self.con.eval_con(x.tolist())}

        bound = [0.0, 1.0]
        self.bounds = np.asarray([bound]*self.num_x)

        # determining the magnitude of the largest initial point
        max_initial = max(self.con.example)
        if max_initial == 0.0:
            self.alpha = 1.0
        else:
            self.alpha = 1.0/max_initial


    def solve(self):
        
        x0_all = np.random.random_sample((self.n_results*2, self.num_x))/self.alpha

        output = []
        cnt = 0
        for i in range(len(x0_all)):
            x0 = x0_all[i, :]

            if self.con.apply(x0.tolist()):
                x_feasible = x0
            else:
                try: 
                    res = self.optimize_feasible(x0)
                    x_feasible = res.x

                    if res.status != 0 or any(x_feasible < 0.0) or any(x_feasible > 1.0) or list(x_feasible) in output:
                        continue

                except:
                    continue

            # if self.con.apply(x_feasible.tolist()):
            #     print "True"
            
            with open(self.outfile, 'a') as f: 
                f.write(" ".join(map(str, x_feasible))) 
                f.write("\n") 

            output.append(list(x_feasible))

            cnt += 1
            if cnt == self.n_results:
                break

        return output                    

    def optimize_feasible(self, x0):
        res = optimize.minimize(self.f, x0, method='SLSQP', 
                       constraints=[self.ineq_cons], options={'ftol': 1e-8, 'disp': False},
                       bounds=self.bounds)
        
        return res

    def f(self, x):
        constr = self.con.eval_con(x.tolist())
        constr[np.where(constr>0)] = 0
        return np.sum(np.square(constr))

    def constraint(self, x):
        constr = self.con.eval_con(x.tolist())
        return constr



if __name__ == "__main__":

    fname = sys.argv[1]
    outfile = sys.argv[2]
    n_results = int(sys.argv[3])
    plot_tf = bool(sys.argv[4])
        
    start = time.time()

    sol_obj = Solution(fname, outfile, n_results) 
    output = sol_obj.solve()

    end = time.time()
    duration = end-start

    if plot_tf: 
        import matplotlib.pyplot as plt
        for i in range(sol_obj.num_x): 
            column = np.array([output[j][i] for j in range(len(output))])
            plt.plot(column, np.zeros_like(column)+i , 'bo')

        plt.xlabel('X values', fontsize=12)
        plt.ylabel('Index of the variable in X', fontsize=12)
        plt.title("Distribution of Solution for "+fname, fontsize=16)
        
        
        plt.yticks(np.arange(0, sol_obj.num_x+1, step=1.0))
        
        plt.show()

    # with open(sol_obj.outfile , 'a') as f:
    #     f.write("==================\n") 
    #     f.write("Elapsed time in seconds: " + "%s\n" % duration) 

    print 'Completed in %s seconds'%duration


