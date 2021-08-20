import matplotlib.pyplot as plt

for j in range(360):

    filename = ['plots/i_', str(j), '.png']

    x = (
    -3, -3, -3, -3, -0.1, 0.1, 3, 3, 3, 3, 0.1, -0.1, -0.1, -0.1, 0.1, 0.1, -3, -3, -3, -3, -0.1, 0.1, 3, 3, 3, 3, 0.1,
    -0.1, -0.1, -0.1, 0.1, 0.1)
    y = (
    3, 0.1, -0.1, -3, -3, -3, -3, -0.1, 0.1, 3, 3, 3, 0.1, -0.1, -0.1, 0.1, 3, 0.1, -0.1, -3, -3, -3, -3, -0.1, 0.1, 3,
    3, 3, 0.1, -0.1, -0.1, 0.1)
    z = (-6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6)
    labels = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    31)
    labels_str = []
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    for i in range(len(x)):
        ax.scatter3D(x[i], y[i], z[i], color='k', marker="s", s=2)
        ax.text(x[i], y[i], z[i], '%s' % (labels[i]), size=5, zorder=2, color='k')

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_zlabel("z [m/s]")
    ax.grid(False)
    ax.view_init(30, j)

    plt.savefig(''.join(filename), dpi=500)
    print(j)
    plt.close()



