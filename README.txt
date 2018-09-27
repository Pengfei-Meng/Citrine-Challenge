1. Instructions on using the code:
    1) To download the repo, use: 
            git clone git@github.com:Pengfei-Meng/Citrine-Challenge.git
       or simply download the zip. 

    2) To run the executable, type the following under the ./Citrine-Challenge/ folder on a Linux/Unix terminal: 
             ./sampler inputfile  outputfile  n_results , 
       e.g.  ./sampler mixture.txt  output_mixture.txt  1000

       if the file show up with non-executable permissions, try the following command:
            chmod u+x sampler
       then retry the previous command for running it. 

    3) Python, Numpy and Scipy are needed to properly run the code. 

    4) If still not working, please contact pengfei.meng.6@gmail.com. 


2. Brief explanation of the solution: 

This challenge can be treated as an optimization problem using random starting points. First it generates "n_results" number of uniformly distributed points in the unit hypercube. Then for each point, if it's feasible it'll be saved. If not, one round of optimization is run to find a feasible point which is saved. 

The definition of the optimization problem is as follows:

objective:  square sum of constriant violations  
subject to:  as defined in the input file

Inside the supporting python class "constraints.py", a class funciton is added that output the values of the constraints and is used heavily. Another function computing the constraint gradients using finite difference is also added but not used. 

Note: for the "alloy.txt", the solution points seem clustered around certain points. 
It could be because it subjects to only bound constraints, and the ranges are very tight. In particular, the scale of the feasible box are in the order of 1e-4 to 1e-1. So ill-conditioning could be an issue.  


3. Brief explanation of past attempts: 

Below is what I experimented but didn't work out per speed requirement(5 mins for 1000 cases). 

    1). Brute force sampling using uniform distribution or normal distribution, save the point if feasible, otherwise continue. 
        Cons: really slow for two of the input files, take more than 10 minutes. 

    2). Intelligent sampling by using the constraint gradients:
        Starting from the given feasible point, compute the constraint gradients. 
        Extract the active constraint gradients. 
        Compute the null space of the active constraint gradient. 
        The new potential steps are constructed using the range space and the null space 
        of the active constraint gradients 

        Check each potential points, save the point if feasible. 

        Cons: still slow sometimes.



