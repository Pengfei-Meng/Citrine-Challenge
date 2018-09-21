#!/usr/bin/env python
import sys, copy, math, random, pdb
from collections import deque
from constraints import Constraint

class Solution():

    def getVector(self, con, n_results=10):

        x = con.example
        # grad_x = con.eval_grad(x)
        num_x = con.n_dim

        out = []
        queue = deque()
        queue.append(x)

        
        # norm_x = math.sqrt(sum([x[i]**2 for i in range(num_x)]))
        # norm_x = max(1e-3, norm_x)
        # increment = norm_x
        pool_dim = 100
        popu = range(1, pool_dim+1)
        population = [popu[i]*1.0/pool_dim for i in range(pool_dim)]

        i = 0
        while queue and i < n_results:
            cur = queue.popleft()

            print i

            if con.apply(cur) and cur not in out:
                out.append(cur)
                i += 1

            constr = con.eval_con(cur)
            constr_grad = con.eval_grad(cur)

            # new_x = []

            idx_rdm = 0

            while idx_rdm < num_x:
                random_dx = random.sample(population, num_x)

                # new_constr = [0]*len(constr)
                # constr + constr_grad * dx >= 0 ? 

                dCdx = [0]*len(constr)
                for i_con in range(len(constr)):

                    dCdx[i_con] = sum([constr_grad[i_con][j]*random_dx[j] for j in range(num_x)])
                    # new_constr[i_con] = constr[i_con] + temp

                    if dCdx[i_con] < 0:
                        break

                if i_con != len(constr)-1:
                    continue

                for idx_radius in range(1, 11):
                    new_x = [x[j] + idx_radius * random_dx[j] for j in range(num_x)]
                    queue.append(new_x)

                idx_rdm += 1

            print new_x


        return out


if __name__ == "__main__":
    
    fname = 'mixture.txt'
    # fname = 'example.txt'
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


