import time


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

    def isempty(self):

        return not self._list

    def empty(self):

        self._list = []


class RunningTask:
    def __init__(self):

        self._running = True

    def terminate(self):

        self._running = False

    def run(self, function):

        while self._running:

            start_time = time.time()

            function()

            end_time = time.time()
            diff_time = end_time - start_time

            if diff_time < 1:

                time.sleep(1 - diff_time)
