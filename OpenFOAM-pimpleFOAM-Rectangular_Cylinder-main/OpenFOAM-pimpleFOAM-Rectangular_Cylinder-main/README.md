# OpenFOAM-pimpleFOAM-Rectangular_Cylinder
2d, komegasst turbulent flow around a rectangular cylinder. 2 cases; case 1 Re=5e5, case 2 Re=5e7
mesh specified using blockMesh only

## to run each case use the following commands

**serial run**
- blockMesh 
- pimpleFoam 
- touch open.foam

**parallel run**
- blockMesh
- decomposePar
- mpirun -np 6 pimpleFoam -parallel
- reconstructPar
- touch open.foam

