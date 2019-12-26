import unittest
import library


class TestBufferQueue(unittest.TestCase):
    def setUp(self):

        self.maxsize = 10
        self.queue = library.BufferQueue(maxsize=self.maxsize)

    def test_bufferQueue(self):

        self.assertEqual(self.queue.isempty(), True, 'Not empty.')
        self.assertRaises(IndexError, self.queue.get)

        for element in range(self.maxsize):

            self.queue.put(element)

        self.assertEqual(self.queue.isempty(), False, 'Empty.')
        self.assertEqual(len(self.queue), self.maxsize, 'Wrong size.')
        self.assertEqual(self.queue.get(), self.maxsize - 1, "Wrong element.")
        self.assertEqual(len(self.queue), self.maxsize - 1, 'Wrong size.')

        self.queue.put(self.maxsize - 1)
        self.queue.put(self.maxsize)

        self.assertEqual(len(self.queue), self.maxsize, 'Wrong size.')
        self.assertEqual(self.queue.get(), self.maxsize, "Wrong element.")
        self.assertEqual(len(self.queue), self.maxsize - 1, 'Wrong size.')

    def tearDown(self):

        del self.queue


if __name__ == '__main__':
    unittest.main()
