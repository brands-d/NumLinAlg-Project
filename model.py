"""Models (MVC pattern) for numerical solutions of differential equations.

This module defines the model used in the MVC pattern (Model-View-Controller)
for a program disgned to solve and display numerical solutions to for example
the stationary heat equation. This module contains an abstract model as well
as concret implementations.
"""

from abc import ABCMeta, abstractmethod
import numpy as np
import controller
import decorator
import library


class AbstractModel():
    """Abstract class defining basic behaviour of models.

    Defines basic beheaviour and interface for all models. Provides simple
    methods common to all models like setting data.

    Args:
        control (AbstractController): Controller (MVC pattern).

    Attributes:
        count_iteration: A positive integer about the current iterations step.
        max_history: An positive integer determining the maximal length of
            history.
        _data: A numpy array containing the data at the current iterations
            step.
        _matrix: A numpy array representing the numerical finite element
            solution to the differential equation. Needs to be
            defined / calculated by each concret model implementation as it
            is depending on the differential equation.
        _data_history: BufferQueue holding the history of the data up to a
            certain maximum (see max_history).
    """

    __metaclass__ = ABCMeta

    def __init__(self, controller, max_history):

        self.controller = controller
        self.count_iteration = 0
        self.max_history = max_history
        self._matrix = None
        self._data = np.array([], dtype=np.float_)
        self._data_history = library.BufferQueue(maxsize=self.max_history)
        self.initial = np.array([], dtype=np.float_)

    @property
    def controller(self):
        """AbstractController: A reference to the controller (MVC pattern)."""

        return self._controller

    @controller.setter
    def controller(self, value):

        if isinstance(value, controller.AbstractController):

            self._controller = value

        else:

            raise TypeError(
                'Needs to be a valid instance of AbstractController.')

    @property
    def initial(self):
        """numpy array (float_): Contains the initial condition of the data."""

        return self._initial

    @initial.setter
    def initial(self, value):

        self._initial = np.array(value, dtype=np.float_)

        # Changing initial condition resets data
        self.reset()

    def current(self):
        """Returns the current state of data.

        Note:
            This method acts like the getter for the data property.
            No iterator!

        Returns:
            numpy array (float_): The data in the current iteration step. If
            no initial and boundary condition has been loaded yet, it will
            return an empty numpy arry.
        """

        return self._data, self._parameters()

    def forward(self):
        """Advances the simulations by one step and returns the new data
        state.

        Note:
            Iterator.

        Returns:
            numpy array (float_): The data in the next iteration step.
        """

        while True:

            self._data_history.put(self._data)

            self._step_forward()
            self.count_iteration += 1

            yield self._data, self._parameters()

    def backward(self):
        """Backtracks the simulations by one step and returns the old data
        state. Doesn't go back and yields current data state if end of history
        has been reached.

        Note:
            Iterator.

        Returns:
            numpy array (float_): The data in the last iteration step. Returns
            current data state if end of history has been reached.
        """

        while True:

            try:

                self._data = self._data_history.pop()
                self.count_iteration -= 1

            except IndexError:

                # End of history has been reached
                pass

            yield self._data, self._parameters()

    def reset(self):

        self.count_iteration = 0
        self._data = self.initial.copy()
        self._data_history.empty()

    @abstractmethod
    def _update_matrix(self):
        pass

    @abstractmethod
    def _step_forward(self):
        pass

    @abstractmethod
    def _parameters(self):
        pass


class LaplaceModel(AbstractModel):
    """Class defining a model solving the laplace equation.

    Model for iterative solving the laplace differential equation. It utilises
    finite element methods to iteratively solving the equation.

    Args:
        control (AbstractController): Controller (MVC pattern).
        max_history (positive integer, optional): The maximal size of the data
            history. See AbstractController for further information.
    """
    def __init__(self, controller, max_history=100):

        super().__init__(controller, max_history)
        self.boundary = np.array([], dtype=np.bool_)

    @property
    def boundary(self):
        """numpy array (bool_): Needs to be same size as initial condition
        and designates which positions are boundaries (= True) and which are
        not (= False). Boundaries to not change during iterations. Outer edge
        in each dimensions needs to be defined as boundary."""

        return self._boundary

    @boundary.setter
    def boundary(self, value):

        value = np.array(value, dtype=np.bool_)

        if value.shape != self.initial.shape:

            raise TypeError(
                "Boundary condition needs to have the same size as initial "
                "condition. ({} != {})".format(value.shape,
                                               self.initial.shape))

        # Testing whether the edge is defined as boundary. Necessary for
        # iteration method to work.
        # Mask for the edge
        edge = np.ones(value.shape, dtype=np.bool_)
        # Slice in arbitrary dimensions for inner part
        index = (slice(1, -1), ) * value.ndim
        edge[index] = False

        if value[edge].all():

            self._boundary = value
            self._update_matrix()

        else:

            raise TypeError('Edge needs to be defined as such.')

    def _update_matrix(self):
        """Updates the matrix A defining the the problem and used for solving
        the differential equation by means of linear algebra.

        Note:
            This method is for internal use only. Pleae don't use this method.
        """

        ndim = self.initial.ndim
        size = self.initial.size
        shape = self.initial.shape

        if size == 0:

            # Catch empty initial data early to avoid errors later on
            self._matrix = np.array([], dtype=np.float_)
            return

        boundary_aux = self.boundary.ravel()
        normalisation = 1 / (2 * ndim)
        self._matrix = np.zeros((size, size), dtype=np.float_)
        # Indicies for the neighbouring elements.
        index = np.array(np.cumprod(shape) / shape[0], dtype=np.int)

        # Goes through all points
        for idx, point in enumerate(self._matrix):

            if boundary_aux[idx]:

                # Boundary conditions should not change
                point[idx] = 1

            else:

                # Neighbouring points
                point[idx + index] = normalisation
                point[idx - index] = normalisation

    @decorator.logThis(filename=None)
    def _step_forward(self):
        """Advances the simulations by one step and returns the new data
        state.

        Note:
            This method is for internal use only. Please use forward()
            instead.
        """
        data_aux = self._data.flatten()
        data_aux = self._matrix.dot(data_aux)

        self._data = np.reshape(data_aux, self._data.shape)

    def _parameters(self):

        try:

            last_data = self._data_history.last()

        except IndexError:

            last_data = self._data.copy()

        mean = np.nanmean(self._data)
        iter_step = self.count_iteration
        abs_change = np.nansum(np.abs(self._data - last_data))
        rel_change = abs_change / (mean * self._data.size)

        parameters = {
            'Average Temperature': mean,
            'Iteration Step': iter_step,
            'Absolute Change': abs_change,
            'Relative Change': rel_change
        }

        return parameters


class LorenzModel(AbstractModel):
    def __init__(self, controller, max_history=10000):

        super().__init__(controller, max_history)
        self.sys_params = {'timeStep': 0, 'sigma': 0, 'rho': 0, 'beta': 0}

    def _update_matrix(self, timeStep=0, sigma=0, rho=0, beta=0):

        self.sys_params.update({
            'timeStep': timeStep,
            'sigma': sigma,
            'rho': rho,
            'beta': rho
        })

        self._matrix = np.array([[1 - timeStep * sigma, sigma * timeStep, 0],
                                 [timeStep * rho, 1 - timeStep, 0],
                                 [0, 0, 1 - timeStep * beta]])

    @decorator.logThis(filename=None)
    def _step_forward(self):

        self._matrix[1, 2] = -self.sys_params['timeStep'] * self._data[0]
        self._matrix[2, 0] = self.sys_params['timeStep'] * self._data[1]
        self._data = self._matrix.dot(self._data)

    def _parameters(self):

        return self.sys_params


class ThreeBodyModel(AbstractModel):
    def __init__(self, controller, max_history=10000):

        super().__init__(controller, max_history)
        self.sys_params = {'timeStep': 0, 'G': 0, 'm_1': 0, 'm_2': 0, 'm_3': 0}

    def _update_matrix(self, timeStep=0, G=0, m_1=0, m_2=0, m_3=0):

        self.sys_params.update({
            'timeStep': timeStep,
            'G': G,
            'm_1': m_1,
            'm_2': m_2,
            'm_3': m_3
        })

        self._matrix = np.eye(18)

        self._matrix[0, 9] = timeStep / m_1
        self._matrix[1, 10] = timeStep / m_1
        self._matrix[2, 11] = timeStep / m_1
        self._matrix[3, 12] = timeStep / m_2
        self._matrix[4, 13] = timeStep / m_2
        self._matrix[5, 14] = timeStep / m_2
        self._matrix[6, 15] = timeStep / m_3
        self._matrix[7, 16] = timeStep / m_3
        self._matrix[8, 17] = timeStep / m_3

    @decorator.logThis(filename=None)
    def _step_forward(self):

        f = self.sys_params['G'] * self.sys_params['timeStep']
        m_1 = self.sys_params['m_1']
        m_2 = self.sys_params['m_2']
        m_3 = self.sys_params['m_3']
        data, _ = self.current()
        r_12 = np.abs(np.linalg.norm(data[0:3] - data[3:6]))**3
        r_13 = np.abs(np.linalg.norm(data[0:3] - data[6:9]))**3
        r_23 = np.abs(np.linalg.norm(data[3:6] - data[6:9]))**3

        for i, row in enumerate(self._matrix[9:12]):
            row[i] = -f * (m_2 / r_12 + m_3 / r_13)
            row[i + 3] = f * m_2 / r_12
            row[i + 6] = f * m_3 / r_13

        for i, row in enumerate(self._matrix[12:15]):
            row[i] = f * m_1 / r_12
            row[i + 3] = -f * (m_1 / r_12 + m_3 / r_23)
            row[i + 6] = f * m_3 / r_23

        for i, row in enumerate(self._matrix[15:18]):
            row[i] = f * m_1 / r_13
            row[i + 3] = f * m_2 / r_23
            row[i + 6] = -f * (m_1 / r_13 + m_2 / r_23)

        self._data = self._matrix.dot(self._data)

    def _parameters(self):

        return self.sys_params