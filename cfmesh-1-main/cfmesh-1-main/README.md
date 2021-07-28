# Notes

## File Structure:
- Main
	- constant
		- polyMesh
		- boundary
		- faces
		- meshMetaDict
		- neighbour
		- owner
		- points
	- system
		- controlDict
		- fvSchemes
		- fvSolution
		- meshDict
	- original.stl
	- bounding_box.stl
	- combined.stl
	- mesh.foam


## Commands:
- **generate bounding box geometry** : surfaceGenerateBoundingBox original.stl bounding_box.stl x_neg x_pos y_neg y_pos z_neg z_pos
	- ex. "surfaceGenerateBoundingBox cube.stl geometry.stl 1 1 0 1 2 1"
- **create mesh**: cartesianMesh
- **create foam file**: touch mesh.foam

