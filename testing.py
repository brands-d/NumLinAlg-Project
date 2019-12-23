from PyQt5 import QtWidgets, uic
import sys
import model
import controller
import numpy as np
import matplotlib.pyplot as plt

ndim = 50
niter = 1000

initial_condition = np.zeros((ndim, ndim), dtype=np.float_)
initial_condition[[0, -1], :] = 1
initial_condition[int(ndim / 2) - 3:int(ndim / 2) + 3,
                  int(ndim / 2) - 3:int(ndim / 2) + 3] = 1
boundary_condition = np.ones((ndim, ndim), dtype=np.bool_)
boundary_condition[1:-1, 1:-1] = False
boundary_condition[int(ndim / 2) - 3:int(ndim / 2) + 3,
                   int(ndim / 2) - 3:int(ndim / 2) + 3] = True

model = model.LaplaceModel(controller.AbstractController())
model.setInitialCondition(initial_condition=initial_condition,
                          boundary_condition=boundary_condition)

model.iterate(niter=niter)
result = model._data

fig, ax = plt.subplots()
plot = plt.imshow(result, cmap='hot', interpolation='nearest')
fig.colorbar(plot, ax=ax)
plt.show()