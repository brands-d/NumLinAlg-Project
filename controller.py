"""Controller (MVC pattern) for numerical solutions of differential equations.

This module defines the controller used in the MVC pattern
(Model-View-Controller) for a program disgned to solve and display numerical
solutions to for example the stationary heat equation. This module contains
an abstract controller as well as concret implementations.
"""

from abc import ABCMeta, abstractmethod
import model
import view
import numpy as np
import library
from threading import Thread


class AbstractController():

    __metaclass__ = ABCMeta

    def __init__(self):

        self.model = None
        self.view = None

    @property
    def model(self):

        return self._model

    @model.setter
    def model(self, value):

        if isinstance(value, model.AbstractModel) or value is None:

            self._model = value

        else:

            raise TypeError('Needs to be a valid instance of AbstractModel.')

    @property
    def view(self):

        return self._view

    @view.setter
    def view(self, value):

        if isinstance(value, view.AbstractView) or value is None:

            self._view = value

        else:

            raise TypeError('Needs to be a valid instance of AbstractView.')

    @abstractmethod
    def stepping(self):
        pass


class Controller(AbstractController):
    def __init__(self):

        self.thread = Thread()
        self.task = None

        super().__init__()

    def stepping(self):

        stepsize = self.view.speed()
        sender = self.view.sender().objectName()

        if stepsize == np.inf:

            # np.inf means realtime -> only one step
            stepsize = 1

        if sender == self.view.gui_list['Forward Step']:

            self._step_forward(stepsize=stepsize)

        elif sender == self.view.gui_list['Backward Step']:

            self._step_backward(stepsize=stepsize)

    def _step_forward(self, stepsize=1):

        for _ in range(stepsize):

            data = next(self._forward_gen)

        self.view.update_plot(data)

    def _step_backward(self, stepsize=1):

        for _ in range(stepsize):

            data = next(self._backward_gen)

        self.view.update_plot(data)

    def load(self):

        initial_condition_file_default = 'testdata_initial'
        boundary_condition_file_default = 'testdata_boundary'

        initial_condition = np.loadtxt(initial_condition_file_default,
                                       dtype=np.float_,
                                       delimiter=',')
        boundary_condition = np.loadtxt(boundary_condition_file_default,
                                        dtype=np.bool_,
                                        delimiter=',')
        self.model.initial = initial_condition
        self.model.boundary = boundary_condition

        self._forward_gen = self.model.forward()
        self._backward_gen = self.model.backward()

        data = self.model.current()
        self.view.update_plot(data)

    def play(self):

        if self.thread.is_alive():

            self.task.terminate()
            self.thread.join()

        else:

            self.task = library.TimedTask()

            # Speed returns steps per second
            desired_run_time = 1 / self.view.speed()

            self.thread = Thread(target=self.task.run,
                                 args=(
                                     self._step_forward,
                                     desired_run_time,
                                 ))
            self.thread.start()

    def kill_processes(self):

        if self.task is not None:

            self.task.terminate()
            self.thread.join()

    def reset(self):

        self.model.reset()
        data = self.model.current()

        self.view.update_plot(data)

    def speed_changed(self):

        if self.thread.is_alive():

            self.play()
            self.play()