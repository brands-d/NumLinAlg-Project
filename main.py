import sys

from PyQt5 import QtWidgets, uic
from view import HeatView, LorenzView, ThreeBodyView
from controller import Controller, LorenzController
from model import LaplaceModel, LorenzModel, ThreeBodyModel


def main():

    app = QtWidgets.QApplication(sys.argv)

    program_type = str.lower(str(sys.argv[1]))

    if program_type == 'heat':

        controller = Controller()
        view = HeatView(controller)
        model = LaplaceModel(controller)

    elif program_type == 'lorenz':

        controller = LorenzController()
        view = LorenzView(controller)
        model = LorenzModel(controller)

    elif program_type == 'three':

        controller = LorenzController()
        view = ThreeBodyView(controller)
        model = ThreeBodyModel(controller)

    else:

        return

    controller.view = view
    controller.model = model

    app.exec_()

    controller.kill_processes()


if __name__ == "__main__":
    main()
