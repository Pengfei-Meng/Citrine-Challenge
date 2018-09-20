import copy

class Constraint():
    """Constraints loaded from a file."""

    def __init__(self, fname):
        """
        Construct a Constraint object from a constraints file

        :param fname: Name of the file to read the Constraint from (string)
        """
        with open(fname, "r") as f:
            lines = f.readlines()
        # Parse the dimension from the first line
        self.n_dim = int(lines[0])
        # Parse the example from the second line
        self.example = [float(x) for x in lines[1].split(" ")[0:self.n_dim]]

        # Run through the rest of the lines and compile the constraints
        self.exprs = []
        self.exprs_val = []
        for i in range(2, len(lines)):
            # support comments in the first line
            if lines[i][0] == "#":
                continue

            idx = lines[i].find('>=')
            self.exprs.append(compile(lines[i], "<string>", "eval"))
            self.exprs_val.append(compile(lines[i][:idx], "<string>", "eval"))
        return

    def get_example(self):
        """Get the example feasible vector"""
        return self.example

    def get_ndim(self):
        """Get the dimension of the space on which the constraints are defined"""
        return self.n_dim

    def apply(self, x):
        """
        Apply the constraints to a vector, returning True only if all are satisfied

        :param x: list or array on which to evaluate the constraints
        """
        for expr in self.exprs:
            if not eval(expr):
                return False
        return True  

    def eval_con(self, x):
        out = []
        for expr in self.exprs_val:
            out.append(eval(expr))
        return out 


    def eval_grad(self, x):

        constr0 = self.eval_con(x)
        num_constr = len(constr0)
        EPS = 1e-7

        Jacobian = [[0]*self.n_dim for _ in range(num_constr)]

        for i in range(self.n_dim):
            x_perturb = copy.deepcopy(x)

            dx = EPS if x[i] == 0.0 else x[i]*EPS
            x_perturb[i] = x[i] + dx

            constr = self.eval_con(x_perturb)


            for j in range(num_constr):
                Jacobian[j][i] = (constr[j] - constr0[j])/EPS 
            
        return Jacobian




    
    
