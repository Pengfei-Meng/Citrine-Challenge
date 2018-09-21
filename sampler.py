#!/usr/bin/env python
import sys, copy, math, random, pdb
from collections import deque
from constraints import Constraint


class Solution():

    def getVector(self, con, n_results=1000):

        x = con.example
        num_x = con.n_dim

        out = []
        queue = deque()
        queue.append(x)

        
        pool_dim = 1000
        popu = range(1, pool_dim+1)
        population = [popu[i]*2.0/pool_dim - 1.0 for i in range(pool_dim)]
        population = list(map(lambda x: round(x, 4), population))

        i = 0
        while queue and i < n_results:
            cur = queue.popleft()
            constr = con.eval_con(cur)
            constr_grad = con.eval_grad(cur)


            if con.apply(cur) and cur not in out:
                out.append(cur)
                i += 1

            new_x_candidates = self.span_cube(cur, population, constr_grad)
            

            for new_x in new_x_candidates:
               
                if con.apply(new_x):
                    queue.append([float('%.4f'%item) for item in new_x]);    
                    # queue.append(["%.4f"%item for item in new_x]);    

            # print new_x


        return out

    def span_cube(self, x, population, constr_grad):
        """
        Generate random vectors, 
        """

        num_x = len(x)
        num_candidates = 2**num_x
        num_constr = len(constr_grad)

        out = []
        i = 0

        while i < num_candidates:
            rand = random.sample(population, num_x)

            # check for dc * dx >= 0? This will slow down the process; but let's see
            dcdx = [0]*num_constr
            for i_con in range(num_constr):

                dcdx[i_con] = sum([constr_grad[i_con][j]*rand[j] for j in range(num_x)])
                # new_constr[i_con] = constr[i_con] + temp

                if dcdx[i_con] < 0:
                    break

            if i_con != num_constr - 1:
                continue  

            new_x = [round(x[j]+rand[j], 4) for j in range(num_x)]
            if all( 0 <= xi <= 1.0 for xi in new_x):
                out.append(new_x)
                i += 1

        return out
        


if __name__ == "__main__":
    
    fname = 'mixture.txt'
    # fname = 'example.txt'
    # fname = 'formulation.txt'
    # fname = 'alloy.txt'
    # fname = sys.argv[1]

    con = Constraint(fname)

    out_vectors = Solution().getVector(con)


    outfile = 'output_' + fname
    

    with open(outfile, 'w') as f:
        for item in out_vectors:
            item_str = str(item)[1:-1]
            item_str2 = item_str.replace(',', ' ')
            f.write("%s\n" % item_str2)


    # norm_x = math.sqrt(sum([x[i]**2 for i in range(num_x)]))
    # norm_x = max(1e-3, norm_x)
    # increment = norm_x
