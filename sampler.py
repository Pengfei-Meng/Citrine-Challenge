#!/usr/bin/env python
import sys, copy, math, random, pdb
from collections import deque
from constraints import Constraint
import numpy as np


class Solution():

    def getVector(self, con, n_results=1000):

        x = con.example
        num_x = con.n_dim

        out = []
        queue = deque()
        queue.append(x)

        i = 0
        while queue and i < n_results:
            cur = queue.popleft()
            # constr = con.eval_con(cur)
            # constr_grad = con.eval_grad(cur)

            # pdb.set_trace()
            if con.apply(cur) and cur not in out:
                out.append(cur)
                print cur
                i += 1

            left_dist = np.array(cur)
            right_dist = np.ones(num_x) - np.array(cur)
            cov = np.diag(np.square( (left_dist + right_dist)/2 ))
            
            ii = 0
            while ii < 2**num_x:
                new_x = np.random.multivariate_normal(np.array(cur), cov, 1).flatten()
                # pdb.set_trace()
                if all(new_x >= 0) and all(new_x <= 1.0) and con.apply(new_x.tolist()):
                    queue.append(new_x.tolist());    
                    ii += 1
                # √  csaprint ii

        return out

    def span_cube(self, x, population, constr_grad=0):
        """
        Generate random vectors, 
        """

        num_x = len(x)
        num_candidates = 2**num_x
        # num_constr = len(constr_grad)

        out = []
        i = 0

        while i < num_candidates:
            rand = random.sample(population, num_x)

            # # check for dc * dx >= 0? This will slow down the process; but let's see
            # dcdx = [0]*num_constr
            # for i_con in range(num_constr):

            #     dcdx[i_con] = sum([constr_grad[i_con][j]*rand[j] for j in range(num_x)])
            #     # new_constr[i_con] = constr[i_con] + temp

            #     if dcdx[i_con] < 0:
            #         break

            # if i_con != num_constr - 1:
            #    continue  

            # new_x = [round(x[j]+rand[j], 4) for j in range(num_x)]
            new_x = [round(rand[j], 4) for j in range(num_x)]
            if all( 0 < xi <= 1.0 for xi in new_x):
                out.append(new_x)
                i += 1

        return out
        


if __name__ == "__main__":
    
    # fname = 'mixture.txt'
    # fname = 'example.txt'
    fname = 'formulation.txt'
    # fname = 'alloy.txt'
    # fname = sys.argv[1]

    con = Constraint(fname)

    out_vectors = Solution().getVector(con)

    # for item in out_vectors:
    #     print con.apply(item)

    outfile = 'output_' + fname
    

    with open(outfile, 'w') as f:
        for item in out_vectors:
            item_str = str(item)[1:-1]
            item_str2 = item_str.replace(',', ' ')
            f.write("%s\n" % item_str2)

