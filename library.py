class BufferQueue():
    def __init__(self, maxsize=None):

        self._list = []
        self._maxsize = maxsize

    def put(self, item):

        if self._maxsize is not None and len(self._list) == self._maxsize:

            self._list.pop(0)

        self._list.append(item)

    def get(self):

        return self._list.pop(-1)

    def __len__(self):

        return len(self._list)

    def empty(self):

        return not self._list