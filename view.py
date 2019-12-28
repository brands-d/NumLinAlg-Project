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


class HeatView(AbstractView):

    default_ui_file = 'heatWindow.ui'
    speed_settings = [np.inf, 1, 10, 50, 100]
    gui_list = {
        'Forward Step': 'pushButton_forward',
        'Backward Step': 'pushButton_backward'
    }

    def __init__(self, controller, ui_file=None):

        self._main_plot = None
        self._difference_plot = None
        self._residue_plot = None

        filename = ui_file if ui_file else HeatView.default_ui_file
        super().__init__(controller, filename)

        self.show()

    def update_plot(self, data):

        self._main_plot.setImage(data, pos=[0, 0], scale=[1, 1])

    def _initialise_widgets(self):

        pg.setConfigOption('background', None)
        pg.setConfigOption('foreground', 'k')

        self._main_plot = pg.ImageView(view=pg.PlotItem())
        self._main_plot.view.invertY(False)
        self._main_plot.setPredefinedGradient('thermal')
        self.gridLayout_main_plot.addWidget(self._main_plot)

    def _setup_connections(self):

        self.pushButton_forward.clicked.connect(self.controller.stepping)
        self.pushButton_backward.clicked.connect(self.controller.stepping)
        self.pushButton_start.clicked.connect(self.controller.play)
        self.pushButton_reset.clicked.connect(self.controller.reset)
        self.pushButton_load.clicked.connect(self.controller.load)
        self.comboBox_colormap.currentIndexChanged.connect(
            self._change_color_map)
        self.comboBox_speed.currentIndexChanged.connect(
            self.controller.speed_changed)

    def _change_color_map(self):

        colormap = self.comboBox_colormap.currentText()
        self._main_plot.setPredefinedGradient(colormap)

    def speed(self):

        speed_index = self.comboBox_speed.currentIndex()
        stepsize = HeatView.speed_settings[speed_index]

        return stepsize
