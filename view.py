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
from PyQt5 import QtWidgets, uic


class AbstractView(QtWidgets.QMainWindow):

    __metaclass__ = ABCMeta

    def __init__(self, controller, ui_file):

        self.controller = controller
        self.gui_list = {}

        super(AbstractView, self).__init__()
        uic.loadUi(ui_file, self)

        self._initialise_widgets()
        self._setup_connections()

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
    speed_settings = [1, 10, 50, 100, np.inf]

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

    def _update_plot(self, data):

        self._main_plot.setImage(data, pos=[0, 0], scale=[1, 1])

    def _initialise_widgets(self):

        pg.setConfigOption('background', None)
        pg.setConfigOption('foreground', 'k')

        self._main_plot = pg.ImageView(view=pg.PlotItem())
        self._main_plot.view.invertY(False)
        self._main_plot.setPredefinedGradient('thermal')
        self._main_plot.ui.histogram.hide()
        self._main_plot.ui.roiBtn.hide()
        self._main_plot.ui.menuBtn.hide()
        self.gridLayout_main_plot.addWidget(self._main_plot)

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
        self.pushButton_load.clicked.connect(self.controller.load)
        self.comboBox_speed.currentIndexChanged.connect(
            self.controller.speed_changed)

    def speed(self):

        speed_index = self.comboBox_speed.currentIndex()
        stepsize = HeatView.speed_settings[speed_index]

        return stepsize

    def _update_parameters(self, param):

        self.label_iter_step_value.setText('{0:d}'.format(
            param['Iteration Step']))
        self.label_avg_temp_value.setText('{0:.3f}'.format(
            param['Average Temperature']))
        self.label_abs_change_value.setText('{0:.3f}'.format(
            param['Absolute Change']))
        self.label_rel_change_value.setText('{0:.3f}'.format(
            param['Relative Change']))

    def update(self, data, param, add_data=True):

        self._update_parameters(param)
        self._update_plot(data)
        self._update_residue(
            (param['Iteration Step'], param['Relative Change']),
            add_data=add_data)

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

    def reset(self):

        self._residue_plot.getPlotItem().clear()
        self._residue_plot.addItem(pg.PlotCurveItem())