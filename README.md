# D-Wave-MPB
Test environment for developing D-Wave applications related to Martec Power Bus
## Automatic Branch Allocation
### Purpose
Build an application able to automatically build a MPB configuration having as inputs:
1. The positions and the power consumptions of all the FCUs
1. The positions of the available cabinets for hosting the DCU's
1. The distances  FCU-FCU and FCU-DCU.
The application will be developed in steps, starting with a very simplified problem and adding to it constraint by constraint till reaching the complete problem.
### Step 1: Basic power allocation
In the base configuration, we consider only the allocation of FCU's to branches based on theit power consumption, disregarding all the other problem constraints.

In this way, the problem is a classical **bin packaging**.

Problem definition:
1. There is a set of FDU's, each one with its own power consumption.
1. FCU's shall be allocated to branches, which have a given power budget (same for alle the branches)
1. Minimum set of branches shall be found.

### Step 2: Limited number of FCU per Branch
In this step we introduce the constraint that no more than a maximum set of FCU's can be handled by a branch, disregarding the power consumption.