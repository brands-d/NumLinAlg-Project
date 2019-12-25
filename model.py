import numpy as np
import controller
import decorator
import library


class AbstractModel():
    def __init__(self, controller):

        self._controller = controller
        self._initial = np.array([], dtype=np.float_)
        self._data = np.array([], dtype=np.float_)
        self._boundary = np.array([], dtype=np.bool_)
        self._A = np.array([], dtype=np.float_)
        self._count_iteration = 0

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

    @property
    def _boundary(self):

        return self.__boundary

    @_boundary.setter
    def _boundary(self, value):

        value = np.array(value, dtype=np.bool_)
        ndim = value.ndim
        edge = np.ones(value.shape, dtype=np.bool_)

        if ndim == 1:

            edge[1:-1] = False

        elif ndim == 2:

            edge[1:-1, 1:-1] = False

        elif ndim == 3:

            edge[1:-1, 1:-1, 1:-1] = False

        else:

            raise TypeError('Dimensions needs to be 3 or lower.')

        if value[edge].all() == True:

            self.__boundary = value
            self._updateA()

        else:

            raise TypeError('Outer boundary needs to be defined as such.')

    @property
    def _initial(self):

        return self.__initial

    @_initial.setter
    def _initial(self, value):

        value = np.array(value, dtype=np.float_)

        self.__initial = value
        self._data = self._initial.copy()

    def current(self):

        yield self._data

    def forward(self):

        while True:

            self._stepForward()
            self._count_iteration += 1

            yield self._data

    def _stepForward(self):
        pass

    def backward(self):

        while True:

            if self._count_iteration > 0:

                try:

                    self._stepBackward()
                    self._count_iteration -= 1

                except IndexError:

                    pass

                yield self._data

            else:

                yield self._data

    def _stepBackward(self):
        pass

    def _updateA(self):
        pass

    def setInitialCondition(self, initial_condition=[], boundary_condition=[]):

        initial = np.array(initial_condition, dtype=np.float_)
        boundary = np.array(boundary_condition, dtype=np.bool_)

        if initial.size != 0:

            if (initial.shape == self._boundary.shape) or (
                    initial.shape == boundary.shape):

                self._initial = initial

            else:

                raise TypeError(
                    'Shape of initial_condition does not match boundary_condition'
                )

        if boundary.size != 0:

            if (boundary.shape == self._initial.shape) or (
                    boundary.shape == initial.shape):

                self._boundary = boundary

            else:

                raise TypeError(
                    'Shape of boundary_condition does not match boundary_condition'
                )


class LaplaceModel(AbstractModel):
    def __init__(self, controller):

        self.max_history = 100
        self._data_history = library.BufferQueue(maxsize=self.max_history)

        super().__init__(controller)

    def _updateA(self):

        size = self._initial.size
        ndim = self._initial.ndim
        shape = self._initial.shape
        boundary_aux = self._boundary.ravel()

        factor = 1 / (2 * ndim)
        self._A = np.zeros((size, size), dtype=np.float_)

        for idx in range(size):

            if boundary_aux[idx] == True:

                self._A[idx, idx] = 1
                continue

            if ndim >= 1:

                self._A[idx, idx + 1] = factor
                self._A[idx, idx - 1] = factor

            if ndim >= 2:

                self._A[idx, idx + shape[1]] = factor
                self._A[idx, idx - shape[1]] = factor

            if ndim >= 3:

                self._A[idx, idx + shape[1] * shape[2]] = factor
                self._A[idx, idx - shape[1] * shape[2]] = factor

    @decorator.logThis(filename=None)
    def _stepForward(self):

        self._data_history.put(self._data)

        data_aux = self._data.flatten()
        data_aux = self._A.dot(data_aux)
        self._data = np.reshape(data_aux, self._data.shape)

    def _stepBackward(self):

        self._data = self._data_history.get()
