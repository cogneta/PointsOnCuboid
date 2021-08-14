import unittest
import numpy as np

from backend.parameters import Point, Cuboid, Problem, init_problem
from core.solver import ProblemSolver


class TestCuboid(unittest.TestCase):

    def test_init(self):
        cub = Cuboid(1, 2, 3)
        l, w, h = cub.get_dimension()
        self.assertEqual(1, l)
        self.assertEqual(2, w)
        self.assertEqual(3, h)

    def test_isvalid(self):
        cub = Cuboid(1, 2, 3)
        self.assertTrue(cub.is_valid())
        cub = Cuboid(1, 0, 3)
        self.assertFalse(cub.is_valid())
        cub = Cuboid(-1, 1, 3)
        self.assertFalse(cub.is_valid())


class TestPoint(unittest.TestCase):

    def test_init(self):
        bug = Point(1, 2, 3)
        x, y, z = bug.get_coordinate()
        self.assertEqual(1, x)
        self.assertEqual(2, y)
        self.assertEqual(3, z)

    def test_isvalid(self):
        cub = Cuboid(1, 2, 3)
        bug = Point(0, 2, 3)
        self.assertTrue(bug.is_valid(cub))
        cub = Cuboid(1, 2, 3)
        bug = Point(1, 4, 3)
        self.assertFalse(bug.is_valid(cub))
        cub = Cuboid(-1, 1, 3)
        bug = Point(-1, 1, 3)
        self.assertFalse(bug.is_valid(cub))


class TestProblem(unittest.TestCase):

    def test_init(self):
        problem = init_problem(1, 2, 3, 1, 2, 3, 0, 0, 0)
        l, w, h = problem.room.get_dimension()
        x1, y1, z1 = problem.bug.get_coordinate()
        x2, y2, z2 = problem.lizard.get_coordinate()
        self.assertEqual(1, l)
        self.assertEqual(2, w)
        self.assertEqual(3, h)
        self.assertEqual(1, x1)
        self.assertEqual(2, y1)
        self.assertEqual(3, z1)
        self.assertEqual(0, x2)
        self.assertEqual(0, y2)
        self.assertEqual(0, z2)

        problem = init_problem(1, 2, 3, 1, 2, 3, -1, 0, 0)
        self.assertEqual(problem, None)

    def test_isvalid(self):
        problem = init_problem(1, 2, 3, 1, 2, 3, 0, 0, 0)
        self.assertTrue(problem.is_valid())


class TestProblemSolver(unittest.TestCase):

    def test_init(self):
        problem = init_problem(1, 2, 3, 1, 2, 3, 0, 0, 0)
        solver = ProblemSolver(problem)
        l, w, h = solver.room.get_dimension()
        x1, y1, z1 = solver.bug.get_coordinate()
        x2, y2, z2 = solver.lizard.get_coordinate()
        self.assertEqual(1, l)
        self.assertEqual(2, w)
        self.assertEqual(3, h)
        self.assertEqual(1, x1)
        self.assertEqual(2, y1)
        self.assertEqual(3, z1)
        self.assertEqual(0, x2)
        self.assertEqual(0, y2)
        self.assertEqual(0, z2)

    def test_solver1(self):
        problem = init_problem(1, 1, 1, 1, 1, 1, 1, 1, 1)
        solver = ProblemSolver(problem)
        self.assertEqual(solver.solve(), 0)

    def test_solver2(self):
        problem = init_problem(1, 1, 1, 0, 0, 0, 1, 1, 1)
        solver = ProblemSolver(problem)
        self.assertEqual(solver.solve(), np.sqrt(5))

    def test_solver3(self):
        problem = init_problem(1, 1, 1, 0.5, 0, 0.95, 0, 0.5, 0.95)
        solver = ProblemSolver(problem)
        self.assertGreater(1 - 1e-3, solver.solve())  # We check that the chosen path is the one through the ceiling


if __name__ == '__main__':
    unittest.main()
