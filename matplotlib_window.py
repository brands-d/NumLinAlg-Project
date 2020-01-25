import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MatplotlibPlot(FigureCanvas):
    def __init__(self, parent=None, width=1, height=1, dpi=1000):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class ResiduePlot(MatplotlibPlot):
    def __init__(self):
        super().__init__()

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)


class MyDynamicMplCanvas(MatplotlibPlot):
    def __init__(self, *args, **kwargs):

        MatplotlibPlot.__init__(self, *args, **kwargs)
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.colorbar_exists = False

    def update_plot(self, data):

        dim_x, dim_y, dim_z = data.shape
        XX, YY, ZZ = np.mgrid[:dim_x, :dim_y, :dim_z]

        self.axes.cla()
        plot = self.axes.scatter(XX.ravel(),
                                 YY.ravel(),
                                 ZZ.ravel(),
                                 c=data.ravel(),
                                 cmap=plt.hot())

        if not self.colorbar_exists:
            self.colorbar_exists = True
            self.fig.colorbar(plot)

        self.draw()
