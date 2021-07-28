import ndtamr.NDTree as nd
import ndtamr.AMR as amr
import ndtamr.Vis as vis
import ndtamr.Data as data
from ndtamr.Data import GenericData
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots
import matplotlib.collections as mc


def ndtamr_refine(t,refinements):
    for i in range(refinements):
        print("\niteration:", i)
        amr.refine(t, tol=0.2, extent=1, min_value=1e-2)
        amr.compression(t)
        amr.start_derefine(t)
        #vis.plot(t, grid=True)
    return t


def ndtamr_coordinates(t):
    # Up to this point the code just follows the example from the NDTAMR Github
    grid = vis.generate_grid(t)
    coords = []
    x = []
    y = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            coords.append(grid[i][j])
            x.append(grid[i][j][0])
            y.append(grid[i][j][1])
    return x, y


def mesh_plot(x, y):
    # Create a plot with connectivity data
    # create bounding box (lower left, upper left, upper right, lower right)
    x_connections = []
    y_connections = []
    x_bb = [min(x), min(x), max(x), max(x), min(x)]
    y_bb = [min(y), max(y), max(y), min(y), min(y)]
    plt.figure(figsize=(6, 6))
    plt.plot(x_bb, y_bb, color='orange', linewidth=0.5)
    for k in range(1, len(x)):
        x_con = [x[k - 1], x[k], x[k - 1], x[k - 1]]
        y_con = [y[k], y[k], y[k], y[k - 1]]
        x_connections.append(x_con)
        y_connections.append(y_con)
        plt.plot(x_con, y_con, color='teal', linewidth=0.5)
    x_con = [x[0], x[0]]
    y_con = [y[0], min(y)]
    x_connections.append(x_con)
    y_connections.append(y_con)
    plt.plot(x_con, y_con, color='teal', linewidth=0.5)
    plt.scatter(x[:], y[:], c='black', s=2)
    plt.minorticks_on()
    dims = [0, 1]
    plt.xlabel('$x_{:d}$'.format(dims[0] + 1), fontsize=20)
    plt.ylabel('$x_{:d}$'.format(dims[1] + 1), fontsize=20)
    plt.tick_params(labelsize=16)
    plt.tight_layout()
    return x_connections, y_connections


class Spiral2D(GenericData):
    data_cols = ['value']

    def __init__(self, coords=(0, 0), file=None, data=None):
        GenericData.__init__(self, coords=coords, file=file, data=data)

    def func(self):
        xc, yc = self.coords
        r = np.sqrt(xc ** 1/3 + yc ** 9)  # np.sqrt(xc ** 2 + yc ** 2)
        p = np.arctan2(yc, xc)
        ps = np.log(r / 1) / .2
        xs = r * np.cos(ps)
        ys = r * np.sin(ps)
        res = np.exp(-((xc - xs) ** 2 + (yc - ys) ** 2) / (2 * .3 ** 2))
        if np.isnan(res) or np.isinf(res):
            res = 1
        return res

    def get_refinement_data(self):
        return self.value


t = nd.make_uniform(depth=4,
                    dim=2,
                    data_class=Spiral2D,
                    xmin=(-2, -2), xmax=(2, 2),
                    restrict_func=nd.restrict_datafunc,
                    prolongate_func=nd.prolongate_datafunc)
vis.plot(t, grid=False)
refinements = 0
t = ndtamr_refine(t, refinements)
x, y = ndtamr_coordinates(t)
x_conn, y_conn = mesh_plot(x, y)
vis.plot(t, grid=False)
plt.show()

