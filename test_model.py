import unittest
import model
import controller
import numpy as np
import os


class TestLaplaceModel(unittest.TestCase):
    def setUp(self):

        self.model = model.LaplaceModel(controller.Controller())

    def test_initialisation(self):

        # Test for correct initialisation
        self.assertEqual(self.model.initial.size, 0)
        self.assertEqual(self.model.boundary.size, 0)

    def test_property_initial(self):

        self.model.initial = [1, 0, 0]

        self.assertEqual((self.model.initial == [1, 0, 0]).all(), True)

        data, _ = self.model.current()
        self.assertEqual((data == self.model.initial).all(), True)

    def test_property_boundary(self):

        self.assertRaises(TypeError, self.model.boundary, [1, 0, 1])

        self.model.initial = [1, 1, 1]

        self.assertRaises(TypeError, self.model.boundary, [0, 0, 1])

        self.assertRaises(TypeError, self.model.boundary, [1, 0, 0, 1])

        self.model.initial = [[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                              [[1, 0, 1], [1, 0, 1], [1, 0, 1]],
                              [[1, 1, 1], [1, 1, 1], [1, 1, 1]]]
        self.model.boundary = [[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                               [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
                               [[1, 1, 1], [1, 1, 1], [1, 1, 1]]]

        self.assertEqual((self.model.boundary == [[[1, 1, 1], [1, 1, 1],
                                                   [1, 1, 1]],
                                                  [[1, 1, 1], [1, 0, 1],
                                                   [1, 1, 1]],
                                                  [[1, 1, 1], [1, 1, 1],
                                                   [1, 1, 1]]]).all(), True)

    def test_forward(self):

        self.model.initial = [1, 0, 1]
        self.model.boundary = [1, 0, 1]
        fow_iter = self.model.forward()

        self.assertEqual(([1, 0, 1] == self.model.initial).all(), True)

        data, _ = next(fow_iter)
        self.assertEqual((data == [1, 1, 1]).all(), True)

        data, _ = next(fow_iter)
        self.assertEqual((data == [1, 1, 1]).all(), True)

    def test_backward(self):

        self.model.initial = [1, 0, 1]
        self.model.boundary = [1, 0, 1]
        ba_iter = self.model.backward()
        fow_iter = self.model.forward()

        data, _ = next(ba_iter)
        self.assertEqual((data == [1, 0, 1]).all(), True)

        _ = next(fow_iter)
        data, _ = next(ba_iter)
        self.assertEqual((data == [1, 0, 1]).all(), True)

        for _ in range(self.model.max_history):
            _ = next(fow_iter)

        for _ in range(self.model.max_history):
            _ = next(ba_iter)

        data, _ = self.model.current()
        self.assertEqual((data == [1, 0, 1]).all(), True)

        for _ in range(self.model.max_history + 1):
            _ = next(fow_iter)

        for _ in range(self.model.max_history + 1):
            _ = next(ba_iter)

        data, _ = self.model.current()
        self.assertEqual((data == [1, 1, 1]).all(), True)

    def test_matrix(self):

        self.model.initial = [1, 0, 1]
        self.model.boundary = [1, 0, 1]

        matrix_should = [[1, 0, 0], [0.5, 0, 0.5], [0, 0, 1]]

        self.assertEqual((self.model._matrix == matrix_should).all(), True)

        self.model.initial = [[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                              [[1, 0, 1], [1, 0, 1], [1, 0, 1]],
                              [[1, 1, 1], [1, 1, 1], [1, 1, 1]]]
        self.model.boundary = [[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                               [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
                               [[1, 1, 1], [1, 1, 1], [1, 1, 1]]]

        matrix_slice_should = np.array([
            0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
            1, 0, 0, 0, 0
        ]) / 6
        self.assertEqual((matrix_slice_should == self.model._matrix[13]).all(),
                         True)

    def tearDown(self):

        del self.model


if __name__ == '__main__':
    unittest.main()
