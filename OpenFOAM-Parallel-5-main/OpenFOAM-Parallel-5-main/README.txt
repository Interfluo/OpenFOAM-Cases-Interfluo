===============================================================================
|          Case          | Calculation Time [sec] | Times Faster (normalized) |
|========================|========================|===========================|
|Non-Parallel (1 process)|         292.54         |            1.00           |
|------------------------|------------------------|---------------------------|
|Parallel (2 processes)	 |         147.24         |            1.99           |
|------------------------|------------------------|---------------------------|
|Parallel (3 processes)	 |         125.61         |            2.33           |
|------------------------|------------------------|---------------------------|
|Parallel (4 processes)	 |         110.07         |            2.66           |
|------------------------|------------------------|---------------------------|
|Parallel (5 processes)	 |         111.22         |            2.63           |
|------------------------|------------------------|---------------------------|
|Parallel (6 processes)	 |         108.20         |            2.70           |
===============================================================================

Notes
- must mave decomposeParDict in systems folder
- make sure that n in the coefficients is correct
	- n tells you number of divisions in each principle orthoganol direction (x, y, z)
	- n = (3,2,1) for 6 threads, (2,2,1) for 4 threads, etc...
- run decomposePar command, this creates seperate folders for each thread
- use command: mpirun -np 2 sonicFoam -parallel to run the case
- must recombine data using reconstructPar -latestTime
- then just make the foam file using the touch command and postprocess as usual

Conclusions
The calculation seems to take less time as it is run on more threads, although the performance
increase seams to be sublinear (diminishing returns on investment). I would imagine that performance 
increase would become more and more linear as the size of the problem domain increased. I also 
noticed an anomaly at 5 threads, this is likely due to the fact that I had to split the doamin 
into a 5x1x1 grid because it is an prime number.   