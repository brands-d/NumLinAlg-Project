from model import LorenzModel
from controller import Controller
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np


def main():

    controller = Controller()
    model = LorenzModel(controller)
    model.initial = [1, 1, 1]
    model._update_matrix(param=[0.001, 10, 28, 8 / 3])
    forward_gen = model.forward()
    all_data = []

    for t in range(50000):
        data, _ = next(forward_gen)
        all_data.append(data)

    all_data = np.array(all_data)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot3D(all_data[:, 0], all_data[:, 1], all_data[:, 2])

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


if __name__ == "__main__":
    main()
