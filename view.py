"""View (MVC pattern) for numerical solutions of differential equations.

This module defines the view used in the MVC pattern (Model-View-Controller)
for a program disgned to solve and display numerical solutions to for example
the stationary heat equation. This module contains an abstract view as well
as concret implementations.
"""

from abc import ABCMeta, abstractmethod
import controller
import numpy as np
import pyqtgraph as pg
import matplotlib_window
from PyQt5 import QtWidgets, uic
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
import pyqtgraph.opengl as gl


class AbstractView(QtWidgets.QMainWindow):

    __metaclass__ = ABCMeta

    def __init__(self, controller, ui_file):

        self.controller = controller
        self.gui_list = {}

        super(AbstractView, self).__init__()
        uic.loadUi(ui_file, self)

        self._initialise_widgets()
        self._setup_connections()

    def load(self):

        # Loading initial data
        initial_data_path, _ = QFileDialog.getOpenFileName(
            None, 'Open initial data file', '', 'All Files (*)')

        # Loading boundary data
        boundary_data_path, _ = QFileDialog.getOpenFileName(
            None, 'Open boundary data file', '', 'All Files (*)')

        if initial_data_path != '' and boundary_data_path != '':

            self.controller.load(initial_data_path, boundary_data_path)

        else:
            pass

    @property
    def controller(self):

        return self._controller

    @controller.setter
    def controller(self, value):

        if isinstance(value, controller.AbstractController):

            self._controller = value

        else:

            raise TypeError(
                'Needs to be a valid instance of AbstractController.')

    @abstractmethod
    def update_plot(self, data):
        pass

    @abstractmethod
    def _initialise_widgets(self):
        pass

    @abstractmethod
    def _setup_connections(self):
        pass

    @abstractmethod
    def update_parameters(self, param):
        pass

    @abstractmethod
    def update(self, data, param):
        pass

    @abstractmethod
    def reset():
        pass


class HeatView(AbstractView):

    default_ui_file = 'heatWindow.ui'
    speed_settings = [1, 5, 10, 25, 50, np.inf]

    def __init__(self, controller, ui_file=None):

        self._main_plot = None
        self._difference_plot = None
        self._residue_plot = None

        filename = ui_file if ui_file else HeatView.default_ui_file
        super().__init__(controller, filename)

        self.gui_list = {
            'Forward Step': self.pushButton_forward,
            'Backward Step': self.pushButton_backward,
            'Play Button': self.pushButton_start
        }

        self.show()

    def _initialise_widgets(self):

        self._main_plot = matplotlib_window.MyDynamicMplCanvas(dpi=100)
        self.gridLayout_main_plot.addWidget(self._main_plot)

        pg.setConfigOption('background', None)
        pg.setConfigOption('foreground', 'k')

        self._residue_plot = pg.PlotWidget()
        self._residue_plot.addItem(pg.PlotCurveItem())
        self._residue_plot.showGrid(True, True)
        self._residue_plot.setLogMode(False, True)
        self.gridLayout_residue_plot.addWidget(self._residue_plot)

    def _setup_connections(self):

        self.pushButton_forward.clicked.connect(self.controller.stepping)
        self.pushButton_backward.clicked.connect(self.controller.stepping)
        self.pushButton_start.clicked.connect(self.controller.play)
        self.pushButton_reset.clicked.connect(self.controller.reset)
        self.pushButton_load.clicked.connect(self.load)
        self.comboBox_speed.currentIndexChanged.connect(
            self.controller.speed_changed)

    def _update_parameters(self, param):

        self.label_iter_step_value.setText('{0:d}'.format(
            param['Iteration Step']))
        self.label_avg_temp_value.setText('{0:.3f}'.format(
            param['Average Temperature']))
        self.label_abs_change_value.setText('{0:.3f}'.format(
            param['Absolute Change']))
        self.label_rel_change_value.setText('{0:.3f}'.format(
            param['Relative Change']))

    def _update_residue(self, data, add_data):

        plot = self._residue_plot.getPlotItem().listDataItems()[0]
        previous_data = plot.getData()

        if add_data:

            x, y = previous_data
            new_data = (np.append(x, data[0]), np.append(y, data[1]))

        else:

            x, y = previous_data
            new_data = (x[:-1], y[:-1])

        plot.setData(x=new_data[0],
                     y=new_data[1],
                     pen=pg.mkPen(color='r', width=3))

    def update(self, data, param, add_data=True):

        self._update_parameters(param)
        self._main_plot.update_plot(data)
        self._update_residue(
            (param['Iteration Step'], param['Relative Change']),
            add_data=add_data)

    def reset(self):

        self._residue_plot.getPlotItem().clear()
        self._residue_plot.addItem(pg.PlotCurveItem())

    def speed(self):

        speed_index = self.comboBox_speed.currentIndex()
        stepsize = HeatView.speed_settings[speed_index]

        return stepsize


class LorenzView(AbstractView):

    default_ui_file = 'lorenzWindow.ui'
    speed_settings = [1, 5, 10, 25, 50, np.inf]

    def __init__(self, controller, ui_file=None):

        self._main_plot = None

        filename = ui_file if ui_file else LorenzView.default_ui_file
        super().__init__(controller, filename)

        self.gui_list = {
            'Forward Step': self.pushButton_forward,
            'Backward Step': self.pushButton_backward,
            'Play Button': self.pushButton_start
        }

        self.show()

    def _initialise_widgets(self):

        pg.setConfigOption('background', None)
        pg.setConfigOption('foreground', 'k')

        self._main_plot = pg.PlotWidget()
        self._main_plot.addItem(pg.PlotCurveItem())
        self.gridLayout_main_plot.addWidget(self._main_plot)

    def _setup_connections(self):

        self.pushButton_forward.clicked.connect(self.controller.stepping)
        self.pushButton_backward.clicked.connect(self.controller.stepping)
        self.pushButton_start.clicked.connect(self.controller.play)
        self.pushButton_reset.clicked.connect(self.controller.reset)
        self.pushButton_load.clicked.connect(self.load)
        self.comboBox_speed.currentIndexChanged.connect(
            self.controller.speed_changed)

    def update(self, data, param=None, add_data=True):

        self._main_plot.update_plot(data)

    def speed(self):

        speed_index = self.comboBox_speed.currentIndex()
        stepsize = LorenzView.speed_settings[speed_index]

        return stepsize
