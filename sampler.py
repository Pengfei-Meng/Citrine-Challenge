#!/usr/bin/env python
import sys, copy, math, random, pdb
from collections import deque
from constraints import Constraint

class Solution():

    def getVector(self, con, n_results=10):

        x = con.example
        grad_x = con.eval_grad(x)
        num_x = con.n_dim

        out = []
        queue = deque()
        queue.append(x)

        i = 0
        # norm_x = math.sqrt(sum([x[i]**2 for i in range(num_x)]))
        # norm_x = max(1e-3, norm_x)
        # increment = norm_x

        while queue and i < n_results:
            cur = queue.popleft()
            EPSILON = random.random()

            if con.apply(cur) and cur not in out:
                out.append(cur)

            for k in range(num_x):
                cur_pos = copy.deepcopy(cur)
                cur_neg = copy.deepcopy(cur)

                cur_pos[k] += abs(cur_pos[k])*EPSILON
                cur_neg[k] -= abs(cur_pos[k])*EPSILON 

                queue.append(cur_pos)
                queue.append(cur_neg)

            i += 1

        return out


if __name__ == "__main__":
    
    # fname = 'mixture.txt'
    fname = 'example.txt'
    # fname = 'alloy.txt'
    # fname = sys.argv[1]

    con = Constraint(fname)

    out = Solution().getVector(con)

    print out



    




