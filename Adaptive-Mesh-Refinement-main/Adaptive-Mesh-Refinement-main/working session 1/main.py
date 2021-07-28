import numpy as np
from matplotlib import pyplot as plt


def build_up_b(rho, dt, dx, dy, u, v):
    b = np.zeros_like(u)
    b[1:-1, 1:-1] = (rho * (1 / dt * ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx) + (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) -
                    ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx)) ** 2 - 2 * ((u[2:, 1:-1] - u[0:-2, 1:-1]) / (2 * dy) *
                    (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx)) - ((v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) ** 2))

    # Periodic BC Pressure @ x = 2
    b[1:-1, -1] = (rho * (1 / dt * ((u[1:-1, 0] - u[1:-1, -2]) / (2 * dx) + (v[2:, -1] - v[0:-2, -1]) / (2 * dy)) -
                  ((u[1:-1, 0] - u[1:-1, -2]) / (2 * dx)) ** 2 - 2 * ((u[2:, -1] - u[0:-2, -1]) / (2 * dy) *
                  (v[1:-1, 0] - v[1:-1, -2]) / (2 * dx)) - ((v[2:, -1] - v[0:-2, -1]) / (2 * dy)) ** 2))

    # Periodic BC Pressure @ x = 0
    b[1:-1, 0] = (rho * (1 / dt * ((u[1:-1, 1] - u[1:-1, -1]) / (2 * dx) + (v[2:, 0] - v[0:-2, 0]) / (2 * dy)) -
                 ((u[1:-1, 1] - u[1:-1, -1]) / (2 * dx)) ** 2 - 2 * ((u[2:, 0] - u[0:-2, 0]) / (2 * dy) *
                 (v[1:-1, 1] - v[1:-1, -1]) / (2 * dx)) - ((v[2:, 0] - v[0:-2, 0]) / (2 * dy)) ** 2))
    return b


def pressure_poisson_periodic(p, dx, dy):
    pn = np.empty_like(p)

    for q in range(nit):
        pn = p.copy()
        p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, 0:-2]) * dy ** 2 + (pn[2:, 1:-1] + pn[0:-2, 1:-1]) * dx ** 2) /
                         (2 * (dx ** 2 + dy ** 2)) - dx ** 2 * dy ** 2 / (2 * (dx ** 2 + dy ** 2)) * b[1:-1, 1:-1])

        # Periodic BC Pressure @ x = 2
        p[1:-1, -1] = (((pn[1:-1, 0] + pn[1:-1, -2]) * dy ** 2 + (pn[2:, -1] + pn[0:-2, -1]) * dx ** 2) /
                       (2 * (dx ** 2 + dy ** 2)) - dx ** 2 * dy ** 2 / (2 * (dx ** 2 + dy ** 2)) * b[1:-1, -1])

        # Periodic BC Pressure @ x = 0
        p[1:-1, 0] = (((pn[1:-1, 1] + pn[1:-1, -1]) * dy ** 2 + (pn[2:, 0] + pn[0:-2, 0]) * dx ** 2) /
                      (2 * (dx ** 2 + dy ** 2)) - dx ** 2 * dy ** 2 / (2 * (dx ** 2 + dy ** 2)) * b[1:-1, 0])

        # Wall boundary conditions, pressure
        p[-1, :] = p[-2, :]  # dp/dy = 0 at y = 2
        p[0, :] = p[1, :]  # dp/dy = 0 at y = 0

    return p


# ======================================================================================= #
# variable declarations
nx = 51
ny = 51
nit = 50
c = 1
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
x = np.linspace(0, 2, nx)
y = np.linspace(0, 2, ny)
X, Y = np.meshgrid(x, y)
# ======================================================================================= #
# physical variables
rho = 1.225
nu = .1
F = 1
dt = 0.75 * min(0.25*dx*dx/nu, 0.25*dy*dy/nu,)  # .001
print("dt =", dt)
# ======================================================================================= #
# initial conditions
u = np.zeros((ny, nx))
un = np.zeros((ny, nx))
v = np.zeros((ny, nx))
vn = np.zeros((ny, nx))
p = np.ones((ny, nx))
pn = np.ones((ny, nx))
b = np.zeros((ny, nx))
# ======================================================================================= #
udiff = 1
stepcount = 0
while udiff > .001:
    un = u.copy()
    vn = v.copy()

    b = build_up_b(rho, dt, dx, dy, u, v)
    p = pressure_poisson_periodic(p, dx, dy)

    u[1:-1, 1:-1] = (un[1:-1, 1:-1] - un[1:-1, 1:-1] * dt / dx * (un[1:-1, 1:-1] - un[1:-1, 0:-2]) -
                     vn[1:-1, 1:-1] * dt / dy * (un[1:-1, 1:-1] - un[0:-2, 1:-1]) - dt / (2 * rho * dx) *
                     (p[1:-1, 2:] - p[1:-1, 0:-2]) + nu * (dt / dx ** 2 * (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] +
                     un[1:-1, 0:-2]) + dt / dy ** 2 * (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1])) + F * dt)

    v[1:-1, 1:-1] = (vn[1:-1, 1:-1] - un[1:-1, 1:-1] * dt / dx * (vn[1:-1, 1:-1] - vn[1:-1, 0:-2]) -
                     vn[1:-1, 1:-1] * dt / dy * (vn[1:-1, 1:-1] - vn[0:-2, 1:-1]) - dt / (2 * rho * dy) *
                     (p[2:, 1:-1] - p[0:-2, 1:-1]) + nu * (dt / dx ** 2 * (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] +
                     vn[1:-1, 0:-2]) + dt / dy ** 2 * (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[0:-2, 1:-1])))

    # Periodic BC u @ x = 2
    u[1:-1, -1] = (un[1:-1, -1] - un[1:-1, -1] * dt / dx * (un[1:-1, -1] - un[1:-1, -2]) - vn[1:-1, -1] * dt / dy *
                   (un[1:-1, -1] - un[0:-2, -1]) - dt / (2 * rho * dx) * (p[1:-1, 0] - p[1:-1, -2]) +
                   nu * (dt / dx ** 2 * (un[1:-1, 0] - 2 * un[1:-1, -1] + un[1:-1, -2]) + dt / dy ** 2 *
                   (un[2:, -1] - 2 * un[1:-1, -1] + un[0:-2, -1])) + F * dt)

    # Periodic BC u @ x = 0
    u[1:-1, 0] = (un[1:-1, 0] - un[1:-1, 0] * dt / dx * (un[1:-1, 0] - un[1:-1, -1]) - vn[1:-1, 0] * dt / dy *
                  (un[1:-1, 0] - un[0:-2, 0]) - dt / (2 * rho * dx) * (p[1:-1, 1] - p[1:-1, -1]) +
                  nu * (dt / dx ** 2 * (un[1:-1, 1] - 2 * un[1:-1, 0] + un[1:-1, -1]) + dt / dy ** 2 *
                  (un[2:, 0] - 2 * un[1:-1, 0] + un[0:-2, 0])) + F * dt)

    # Periodic BC v @ x = 2
    v[1:-1, -1] = (vn[1:-1, -1] - un[1:-1, -1] * dt / dx * (vn[1:-1, -1] - vn[1:-1, -2]) - vn[1:-1, -1] * dt / dy *
                   (vn[1:-1, -1] - vn[0:-2, -1]) - dt / (2 * rho * dy) * (p[2:, -1] - p[0:-2, -1]) +
                   nu * (dt / dx ** 2 * (vn[1:-1, 0] - 2 * vn[1:-1, -1] + vn[1:-1, -2]) + dt / dy ** 2 *
                   (vn[2:, -1] - 2 * vn[1:-1, -1] + vn[0:-2, -1])))

    # Periodic BC v @ x = 0
    v[1:-1, 0] = (vn[1:-1, 0] - un[1:-1, 0] * dt / dx * (vn[1:-1, 0] - vn[1:-1, -1]) - vn[1:-1, 0] * dt / dy *
                  (vn[1:-1, 0] - vn[0:-2, 0]) - dt / (2 * rho * dy) * (p[2:, 0] - p[0:-2, 0]) +
                  nu * (dt / dx ** 2 * (vn[1:-1, 1] - 2 * vn[1:-1, 0] + vn[1:-1, -1]) + dt / dy ** 2 *
                  (vn[2:, 0] - 2 * vn[1:-1, 0] + vn[0:-2, 0])))

    # Wall BC: u,v = 0 @ y = 0,2
    u[0, :] = 0
    u[-1, :] = 0
    v[0, :] = 0
    v[-1, :] = 0

    udiff = (np.sum(u) - np.sum(un)) / np.sum(u)
    stepcount += 1
    if stepcount % 100 == 0:
        print(stepcount)
print(stepcount)
# ======================================================================================= #
# Plotting - plot the streamlines and contours of the final velocity field
fig1 = plt.figure(figsize=(11, 7), dpi=100)
plt.quiver(X, Y, u, v)
fig2 = plt.figure(figsize=(11, 7), dpi=100)
ucc = 0.5*(u[1:-1, 2:] + u[1:-1, 1:-1])
vcc = 0.5*(v[2:, 1:-1] + v[1:-1, 1:-1])
speed = np.sqrt(ucc*ucc + vcc*vcc)
plt.contourf(speed[2:-2], levels=100)
plt.colorbar()
fig3 = plt.figure(figsize=(11, 7), dpi=100)
plt.plot(X, Y, ".k")
plt.show()


"""import numpy as np
import discretize
import matplotlib.pyplot as plt

ncx = 2**5  # number of cells in the x-direction
ncy = ncx  # number of cells in the y-direction

# create a tensor mesh
tensor_mesh = discretize.TensorMesh([ncx, ncy])

# create a tree mesh and refine some of the cells
tree_mesh = discretize.TreeMesh([ncx, ncy])


def refine(cell):
    if np.sqrt(((np.r_[cell.center] - 0.5) ** 2).sum()) < 0.2:
        return 4
    return 2


tree_mesh.refine(refine)


# create a curvilinear mesh
curvi_mesh = discretize.CurvilinearMesh(
    discretize.utils.exampleLrmGrid([ncx, ncy], "rotate")
)

# Plot
fig, axes = plt.subplots(1, 3, figsize=(14.5, 4))
tensor_mesh.plotGrid(ax=axes[0])
axes[0].set_title("TensorMesh")

tree_mesh.plotGrid(ax=axes[1])
axes[1].set_title("TreeMesh")

curvi_mesh.plotGrid(ax=axes[2])
axes[2].set_title("CurvilinearMesh")

plt.show()


import gmsh
import sys

gmsh.initialize()
gmsh.model.add("t1")
lc = 1e-2
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
gmsh.model.geo.addPoint(.1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(.1, .3, 0, lc, 3)
p4 = gmsh.model.geo.addPoint(0, .3, 0, lc)
gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addLine(3, 2, 2)
gmsh.model.geo.addLine(3, p4, 3)
gmsh.model.geo.addLine(4, 1, p4)
gmsh.model.geo.addCurveLoop([4, 1, -2, 3], 1)
gmsh.model.geo.addPlaneSurface([1], 1)
gmsh.model.geo.synchronize()
gmsh.model.addPhysicalGroup(1, [1, 2, 4], 5)
ps = gmsh.model.addPhysicalGroup(2, [1])
gmsh.model.setPhysicalName(2, ps, "My surface")
gmsh.model.mesh.generate(2)
gmsh.write("t1.msh")
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()
gmsh.finalize()"""