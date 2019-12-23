import model
import view


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

        return self.__model

    @_view.setter
    def _view(self, value):

        if isinstance(value, view.AbstractView) or value is None:

            self.__view = value

        else:

            raise TypeError('Needs to be a valid instance of AbstractView.')


class Controller(AbstractController):
    def __init__(self):
        super().__init__()