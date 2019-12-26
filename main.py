from PyQt5 import QtWidgets, uic
import sys
from view import HeatView
from controller import Controller
from model import LaplaceModel


def main():
    app = QtWidgets.QApplication(sys.argv)

    controller = Controller()
    view = HeatView(controller)
    model = LaplaceModel(controller)

    controller._view = view
    controller._model = model

    app.exec_()

    controller.killProcesses()


if __name__ == "__main__":
    main()
