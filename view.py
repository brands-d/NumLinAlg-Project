from PyQt5 import QtWidgets, uic
import controller
import pyqtgraph as pg


class AbstractView(QtWidgets.QMainWindow):
    def __init__(self, controller, ui_file):

        self._controller = controller

        super(AbstractView, self).__init__()
        uic.loadUi(ui_file, self)

        self._initialiseWidgets()
        self._setupConnections()

    @property
    def _controller(self):

        return self.__controller

    @_controller.setter
    def _controller(self, value):

        if isinstance(value, controller.AbstractController):

            self.__controller = value

        else:

            raise TypeError(
                'Needs to be a valid instance of AbstractController.')

    def updatePlot(self, data):
        pass

    def _initialiseWidgets(self):
        pass

    def _setupConnections(self):
        pass


class HeatView(AbstractView):

    default_ui_file = 'heatWindow.ui'

    def __init__(self, controller, ui_file=None):

        self._main_plot = None
        self._difference_plot = None
        self._residue_plot = None

        filename = ui_file if ui_file else HeatView.default_ui_file
        super().__init__(controller, filename)

        self.show()

    def updatePlot(self, data, pos=[0, 0], scale=[1, 1]):

        self._main_plot.setImage(data, pos=pos, scale=scale)

    def _changeColorMap(self):

        colormap = self.comboBox_colormap.currentText()
        self._main_plot.setPredefinedGradient(colormap)

    def _initialiseWidgets(self):

        self._main_plot = pg.ImageView(view=pg.PlotItem())
        self._main_plot.view.invertY(False)
        self._main_plot.setPredefinedGradient('thermal')
        self.gridLayout_main_plot.addWidget(self._main_plot)

    def _setupConnections(self):

        self.pushButton_forward.clicked.connect(self._controller.stepForward)
        self.pushButton_backward.clicked.connect(self._controller.stepBackward)
        self.pushButton_load.clicked.connect(self._controller.load)
        self.comboBox_colormap.currentIndexChanged.connect(
            self._changeColorMap)