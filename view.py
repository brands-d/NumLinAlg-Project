from PyQt5 import QtWidgets, uic
import controller


class AbstractView(QtWidgets.QMainWindow):
    def __init__(self, controller, ui_file):

        self._controller = controller

        super(AbstractView, self).__init__()
        uic.loadUi(ui_file, self)

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

    def updatePlot(self):
        pass

    def returnSettings(self):
        pass


class HeatView(AbstractView):

    default_ui_file = 'heatWindow.ui'

    def __init__(self, controller, ui_file=None):

        filename = ui_file if ui_file else HeatView.default_ui_file

        super().__init__(controller, filename)
        self.show()

    def updatePlot(self):
        pass

    def returnSettings(self):
        pass
