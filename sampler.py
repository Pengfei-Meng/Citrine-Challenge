#!/usr/bin/env python
import sys, copy, math, random, pdb
from collections import deque
from constraints import Constraint
import numpy as np
import time

class Solution():

    def getVector(self, fname, n_results=1000):

        
        con = Constraint(fname)
        outfile = 'output_' + fname
        with open(outfile, 'w') as f:   
            f.write("------------------\n")   


        x = con.example
        num_x = con.n_dim

        out = []
        queue = deque()
        queue.append(x)


        i = 0
        while queue and i < n_results:
            # t0 = time.time()

            cur = queue.popleft()
            constr = con.eval_con(cur)
            constr_grad = con.eval_grad(cur)

            constr_lb = constr[:num_x]
            constr_ub = constr[num_x:2*num_x]

            # cov = np.diag(np.square( (constr_lb + constr_ub)/4 ))
            cov = np.diag(np.ones(num_x)/2) 
            
            if con.apply(cur) and cur not in out:
                out.append(cur)
                i += 1

                with open(outfile, 'a') as f:                    
                    item_str = str(cur)[1:-1]
                    item_str2 = item_str.replace(',', ' ')
                    f.write("%s\n" % item_str2)     
                
            # t2 = time.time() 
            # print 't2: ', t2-t0


            num_candidates = 1000 # 2**num_x
            
            # ----------  Generating candidates here  -----------
            active_idx = np.where(constr==0)
            active_grad = constr_grad[active_idx[0], :]
            active_num = len(active_grad)
            
            # pdb.set_trace()
            # print 'active constraints: ', active_num



            ii = 0
            while ii < 2**num_x:
                if active_num > 0:

                    null_active = self.null_space(active_grad)
                    nonactive_num = null_active.shape[0]

                    d_alpha = np.random.random_sample((num_candidates, active_num))/2
                    dx_all = np.dot(d_alpha, active_grad)
                    
                    if nonactive_num > 0:
                        d_alpha2 = np.random.multivariate_normal(np.zeros(nonactive_num), np.diag(np.ones(nonactive_num)/2), num_candidates)
                        dx_all_2 = np.dot(d_alpha2, null_active)
                        dx_all = dx_all + dx_all_2
                
                else:
                    dx_all = np.random.multivariate_normal(np.array(cur), cov, num_candidates)


                for dx in dx_all:
                    new_x = np.array(cur) + dx
                    
                    if all(new_x >= 0) and all(new_x <= 1.0) and con.apply(new_x.tolist()):
                        queue.append(new_x.tolist());
                        ii += 1    

            # ---------------------------------------------------------

            # t3 = time.time() 
            # print 't3: ', t3-t2



    def null_space(self, A):

        m, n = A.shape[0], A.shape[1]

        if n>m:
            A_mat = np.matrix(A.transpose())
        else:
            A_mat = A

        rank = np.linalg.matrix_rank(A_mat)
        U, s, V = np.linalg.svd(A_mat, full_matrices = True)
        t_U_A = np.transpose(U)
        nrow = t_U_A.shape[0]
        left_null_A = t_U_A[rank:nrow,:]
        
        return np.asarray(left_null_A)
        


if __name__ == "__main__":
    
    # fname = 'mixture.txt'
    # fname = 'example.txt'
    fname = 'formulation.txt'
    # fname = 'alloy.txt'
    # fname = sys.argv[1]

    start = time.time()

    Solution().getVector(fname)

    end = time.time()
    duration = end-start

    outfile = 'output_' + fname
    with open(outfile, 'a') as f:
        f.write("==================\n") 
        f.write("Elapsed time in seconds: " + "%s\n" % duration) 

    print 'Completed.'





