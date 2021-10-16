###################################################################################################
# Branch Allocation - Step 1
###################################################################################################

# ------- Import Section -------
import numpy as np
from dimod import ConstrainedQuadraticModel
from dimod import Binary
from dwave.system import LeapHybridCQMSampler

# ------- Program Configuration -------
fcuPowerConsumption = [7, 3, 10, 12, 4, 4, 18, 2]
numFcus = len(fcuPowerConsumption)
branchPowerBudget = 20
numBranches = 4    # Given the above listed FCU, total consumption 60, 4 branches are enough

# ------- Printing Program Data -------
print("Problem: allocate a set of FCU's with total power consumption of {} into branches of capacity {}.".format(
    sum(fcuPowerConsumption), branchPowerBudget))
for i, value in enumerate(fcuPowerConsumption):
    print("---FCU {} : {}".format(i, value))

# ------- Model Configuration -------

# Initialization of CQM
cqm = ConstrainedQuadraticModel()
max_time = 10

# Creation of the list of branch_used variables
branchUsed = [Binary(f'branch_used_{i}') for i in range(numBranches)]

# Objective function: minimise the numeber of branch used
cqm.set_objective(sum(branchUsed))

# Creation of the list of variables to allocate a fcu_<i>_in_branch_<j> 
FcuInBranch = [[Binary(f'fcu_{i}_in_branch_{j}') for j in range(numBranches)] for i in range(numFcus)]

# Constraint 1: Each FDU can go into only one branch
for i in range(numFcus):
    one_branch_per_fcu = cqm.add_constraint(sum(FcuInBranch[i][j] for j in range(numBranches)) == 1, label=f'fcu_placing_{i}')

# Constraint 2: Each branch has limited power budget
for j in range(numBranches):
    FcuUpToCapacity = cqm.add_constraint(
        sum(fcuPowerConsumption[i] * FcuInBranch[i][j] for i in range(numFcus)) - branchUsed[j] * branchPowerBudget <= 0,
        label=f'capacity_branch_{j}')

# Initialization of Hybrid SOlver
sampler = LeapHybridCQMSampler()

# Submit the CQM to the selected solver
sampleset = sampler.sample_cqm(cqm, time_limit=max_time,label="Branch Allocation - Step 1")

# Selection of feasible solutions
feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)  
if len(feasible_sampleset):      
   best = feasible_sampleset.first
   print("{} feasible solutions of {}.".format(len(feasible_sampleset), len(sampleset)))

# Helper function (for subsequent steps)
def get_indices(name):
    return [int(digs) for digs in name.split('_') if digs.isdigit()]

# Analysis of best solution
selected_branches = [key for key, val in best.sample.items() if 'branch_used' in key and val]   
print("{} branches are used.".format(len(selected_branches)))
for branch in selected_branches:                        
    inBranch = [key for key, val in best.sample.items() if
       "_in_branch" in key and 
       get_indices(key)[1] == get_indices(branch)[0]
       and val]
    b = get_indices(inBranch[0])[1]
    w = [fcuPowerConsumption[get_indices(item)[0]] for item in inBranch]
    print("Branch {} has FCU {} for a total of {}.".format(b, w, sum(w)))


