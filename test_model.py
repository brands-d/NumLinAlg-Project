import unittest
import model
import controller
import numpy as np
import os


class TestAbstractModel(unittest.TestCase):
    def setUp(self):

        self.model = model.AbstractModel(controller.AbstractController())

    def test_setInitialCondition(self):

        # Test for correct initialisation
        self.assertEqual(self.model._initial.size, 0,
                         'Initial value of _initial not correct.')
        self.assertEqual(self.model._boundary.size, 0,
                         'Initial value of _boundary not correct.')

        # Test empty usage of setInitialCondition
        self.model.setInitialCondition()

        self.assertEqual(self.model._initial.size, 0,
                         'Empty update of _initial not correct.')
        self.assertEqual(self.model._boundary.size, 0,
                         'Empty update of _boundary not correct.')

        # Test test exceptions thrown when wrong dimension is entered
        self.assertRaises(TypeError,
                          self.model.setInitialCondition,
                          initial_condition=[1, 2, 3])
        self.assertRaises(TypeError,
                          self.model.setInitialCondition,
                          boundary_condition=[1, 2, 3])
        self.assertRaises(TypeError,
                          self.model.setInitialCondition,
                          initial_condition=[1, 2, 3],
                          boundary_condition=[2, 3])

        # Test incorrect boundary condition
        initial_condition = np.zeros((5, 5), dtype=np.float_)
        boundary_condition = np.zeros((5, 5), dtype=np.bool_)

        self.assertRaises(TypeError,
                          self.model.setInitialCondition,
                          initial_condition=initial_condition,
                          boundary_condition=boundary_condition)

        # Test for correct usage
        initial_condition = np.array([[1, 2], [3, 4]], dtype=np.float_)
        boundary_condition = np.array([[5, 6], [7, 8]], dtype=np.bool_)

        self.model.setInitialCondition(initial_condition=initial_condition,
                                       boundary_condition=[[5, 6], [7, 8]])

        self.assertEqual((self.model._initial == initial_condition).all(),
                         True, 'Update of _initial not correct.')
        self.assertEqual((self.model._boundary == boundary_condition).all(),
                         True, 'Update of _boundary not correct.')

    def test_boundaryProperty(self):

        correct_boundary_condition_1 = [1, 1, 1]
        correct_boundary_condition_2 = [[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                                        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
                                        [[1, 1, 1], [1, 1, 1], [1, 1, 1]]]
        incorrect_boundary_condition_1 = [1, 1, 0]
        incorrect_boundary_condition_2 = [[[1, 0, 1], [1, 1, 1], [1, 1, 1]],
                                          [[1, 0, 1], [1, 0, 1], [1, 0, 1]],
                                          [[1, 1, 1], [1, 1, 1], [1, 1, 1]]]
        incorrect_boundary_condition_3 = np.zeros((5, 5), dtype=np.bool_)

        self.model._boundary = correct_boundary_condition_1
        self.model._boundary = correct_boundary_condition_2

        self.assertEqual(
            (self.model._boundary == np.array(correct_boundary_condition_2,
                                              dtype=np.bool_)).all(), True,
            'Update of _initial not correct.')

        self.assertRaises(TypeError,
                          self.model._boundary,
                          boundary_condition=incorrect_boundary_condition_1)
        self.assertRaises(TypeError,
                          self.model._boundary,
                          boundary_condition=incorrect_boundary_condition_2)
        self.assertRaises(TypeError,
                          self.model._boundary,
                          boundary_condition=incorrect_boundary_condition_3)

    def test_intialProperty(self):

        initial_condition = np.random.random((3, 1))

        self.model._initial = initial_condition

        self.assertEqual((self.model._data == self.model._initial).all(), True,
                         'Update of _initial not correct.')

    def tearDown(self):

        del self.model


class TestLaplaceModel(unittest.TestCase):
    def setUp(self):

        self.model = model.LaplaceModel(controller.AbstractController())

    def test__updateA(self):

        boundary_condition_1D = np.array([1, 0, 1], dtype=np.bool_)
        boundary_condition_2D = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]],
                                         dtype=np.bool_)
        boundary_condition_3D = np.array([[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                                          [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
                                          [[1, 1, 1], [1, 1, 1], [1, 1, 1]]],
                                         dtype=np.bool_)

        initial_condition_1D = np.zeros(boundary_condition_1D.shape)
        initial_condition_2D = np.zeros(boundary_condition_2D.shape)
        initial_condition_3D = np.zeros(boundary_condition_3D.shape)

        correct_A_1D = np.array([[1, 0, 0], [1 / 2, 0, 1 / 2], [0, 0, 1]],
                                dtype=np.float_)
        correct_A_2D = np.array(
            [[1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0],
             [0, 1 / 4, 0, 1 / 4, 0, 1 / 4, 0, 1 / 4, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1]],
            dtype=np.float_)
        correct_A_3D_slice = np.array([
            0, 0, 0, 0, 1 / 6, 0, 0, 0, 0, 0, 1 / 6, 0, 1 / 6, 0, 1 / 6, 0,
            1 / 6, 0, 0, 0, 0, 0, 1 / 6, 0, 0, 0, 0
        ],
                                      dtype=np.float_)

        # Test 1D case
        self.model.setInitialCondition(
            initial_condition=initial_condition_1D,
            boundary_condition=boundary_condition_1D)
        self.assertEqual((self.model._A == correct_A_1D).all(), True,
                         "1D case doesn't match")

        # Test 2D case
        self.model.setInitialCondition(
            initial_condition=initial_condition_2D,
            boundary_condition=boundary_condition_2D)

        self.assertEqual((self.model._A == correct_A_2D).all(), True,
                         "2D case doesn't match")

        # Test 3D case
        self.model.setInitialCondition(
            initial_condition=initial_condition_3D,
            boundary_condition=boundary_condition_3D)

        self.assertEqual((self.model._A[13, :] == correct_A_3D_slice).all(),
                         True, "3D case doesn't match")

    def tearDown(self):

        del self.model


if __name__ == '__main__':
    unittest.main()
