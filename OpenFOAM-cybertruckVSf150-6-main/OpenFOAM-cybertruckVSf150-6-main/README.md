# OpenFOAM-pisoFoam-LES-cybertruckVSf150-6

This Repository contains the files for a video I made comparing the aerodynamics of the upcoming Tesla Cybertruck to a more traditional design modeled after a Ford F150. For fun, the aerodynamics of a brick will also be evaluated.
The purpose was not to realistically capture the aerodynamics of either vehicle but to get a rough, first order, approximation to be able to compare them.

Two solvers:
- pisoFoam LES: uses the piso (Pressure Implicit with Splitting of Operator) pressure velocity coupling to solve for a transient flow. My boundary conditions in this analysis are not perfect; I only used these for flow visualization. If you want to use these for a real world application, I would recommend revising the boundary conditions, refining the mesh and adding some orthoganol corrector steps.
- simpleFoam: uses the simple (Semi-Implicit Method for Pressure Linked Equations) pressure velocity coupling to solve a steady state flow. The boundary conditions have been revised for this analysis to obtain better results. I used these results to calculate the Drag force on the object. Again, if you want to use this analysis for a real world application I would recommend refining the mesh.

The general procedure for this project where:
- Generate the Geometry (SolidWorks)
- Meshing (BlockMesh & SnappyHexMesh)
- Specifying Boundary conditions (OpenFOAM)
- Running the Simulation (OpenFOAM)
- Postprocessing (ParaView & Blender)

Boundary Conditions:
- velocity inlet = 132 m/s (equivalent Re to the full-size truck @ 50mph)
- pressure outlet
- walls with slip around the domain
- no slip at the truck surface


               _________________________
              /.                       /|
             / .                      / |
            /  .                     /  |
           /   .                    /   |
          /    .                   /    |
	     /     .                  /     |
	    /      .                 /      |
       /________________________/       |
       |       .................|.......|
       |       .                |       /
       |      .                 |      /
       |     .         __       |     /
       |    .        /__/|      |    /
       |   .         |__|/      |   /
       |  .                     |  /
       | .                      | /
       |._______________________|/
       

Steps to improve the Project:
- model the rotating wheels
- generate more accurate vehicle models
- greatly refine the mesh and increase the domain size

Commands to run any Case:
- blockMesh (create base mesh for domain)
- snappyHexMesh (carve out the geometry and refine)
- decomposePar (decompose the mesh)
- mpirun -np 6 pisoFoam -parallel (run the solver in parallel on 6 cores)
- ReconstructPar (recombine the decomposed results at every time-step)
- touch results.foam (create a results file)
