import model
import view
import numpy as np
import time


class AbstractController():
    def __init__(self):

        self._model = None
        self._view = None

    @property
    def _model(self):

        return self.__model

    @_model.setter
    def _model(self, value):

        if isinstance(value, model.AbstractModel) or value is None:

            self.__model = value

        else:

            raise TypeError('Needs to be a valid instance of AbstractModel.')

    @property
    def _view(self):

        return self.__view

    @_view.setter
    def _view(self, value):

        if isinstance(value, view.AbstractView) or value is None:

            self.__view = value

        else:

            raise TypeError('Needs to be a valid instance of AbstractView.')


class Controller(AbstractController):
    def __init__(self):
        super().__init__()

    def stepForward(self):

        stepsize = self._view.speed()
        stepsize = np.abs(stepsize)

        for _ in range(stepsize):

            data = next(self._model.forward())

        self._view.updatePlot(data)

    def stepBackward(self):

        stepsize = self._view.speed()
        stepsize = np.abs(stepsize)

        for _ in range(stepsize):

            data = next(self._model.backward())

        self._view.updatePlot(data)

    def load(self):

        initial_condition_file_default = 'testdata_initial'
        boundary_condition_file_default = 'testdata_boundary'

        initial_condition = np.loadtxt(initial_condition_file_default,
                                       dtype=np.float_,
                                       delimiter=',')
        boundary_condition = np.loadtxt(boundary_condition_file_default,
                                        dtype=np.bool_,
                                        delimiter=',')
        self._model.setInitialCondition(initial_condition=initial_condition,
                                        boundary_condition=boundary_condition)

        data = next(self._model.current())
        self._view.updatePlot(data)
