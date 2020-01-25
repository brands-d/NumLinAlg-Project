from PyQt5 import QtWidgets, uic
import sys
import model
import controller
import view
import numpy as np
import matplotlib.pyplot as plt
import time
'''
app = QtWidgets.QApplication(sys.argv)
app.exec_()'''

ndim = 50

initial_condition = np.zeros((ndim, ndim), dtype=np.float_)
initial_condition[[0, -1], :] = 1
initial_condition[int(ndim / 2) - 3:int(ndim / 2) + 3,
                  int(ndim / 2) - 3:int(ndim / 2) + 3] = 1
boundary_condition = np.ones((ndim, ndim), dtype=np.bool_)
boundary_condition[1:-1, 1:-1] = False
boundary_condition[int(ndim / 2) - 3:int(ndim / 2) + 3,
                   int(ndim / 2) - 3:int(ndim / 2) + 3] = True

np.savetxt('testdata_initial', initial_condition, delimiter=',', fmt='%u')
np.savetxt('testdata_boundary', boundary_condition, delimiter=',', fmt='%u')
'''
controller = controller.AbstractController()
view = view.HeatView(controller)
model = model.LaplaceModel(controller)
model.setInitialCondition(initial_condition=initial_condition,
                          boundary_condition=boundary_condition)

data_generator = model.iterator()

for data in data_generator:

    time.sleep(1)
    view.update_plot(data)
'''