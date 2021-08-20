import csv
import matplotlib.pyplot as plt


def get_data(filepath):
    X, Z, Uy, Uz = [], [], [], []
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                X.append(float(row[0]))
                Z.append(float(row[1]))
                Uy.append(float(row[2]))
                Uz.append(float(row[3]))
                line_count += 1
        print('processed finished for case: ', filepath)
    return X, Z, Uy, Uz




string = "velocity_data/"

x2, x4, x7 = [], [], []
z2, z4, z7 = [], [], []
uz2, uz4, uz7 = [], [], []
for i in [2, 4, 7]:
    for j in range(1,14):
        filepath = "".join([string, str(i), '/', str(j), '.csv'])
        X, Z, Uy, Uz = get_data(filepath)
        if i == 2:
            for k in range(len(X)):
                x2.append(X[k])
                z2.append(Z[k])
                uz2.append(Uz[k])
        elif i == 4:
            for l in range(len(X)):
                x4.append(X[l])
                z4.append(Z[l])
                uz4.append(Uz[l])
        elif i == 7:
            for m in range(len(X)):
                x7.append(X[m])
                z7.append(Z[m])
                uz7.append(Uz[m])


for j in range(360):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    filename = ['plotsU/i_', str(j), '.png']
    ax.view_init(30, j)
    ax.plot3D(x2, z2, uz2, 'r')
    ax.plot3D(x4, z4, uz4, 'g')
    ax.plot3D(x7, z7, uz7, 'b')
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Z [m]")
    ax.set_zlabel("Uz [m/s]")
    plt.legend(["case 2", "case 4", "case 7"], loc="upper right")
    ax.grid(False)
    plt.savefig(''.join(filename), dpi=500)
    print(j)
    plt.close()