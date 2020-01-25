from PyQt5 import QtWidgets, uic
import sys
from view import HeatView
from controller import Controller
from model import LorenzModel


def main():
    app = QtWidgets.QApplication(sys.argv)

    controller = Controller()
    view = LorenzView(controller)
    model = LorenzModel(controller)

    controller.view = view
    controller.model = model

    app.exec_()

    controller.kill_processes()


if __name__ == "__main__":
    main()
