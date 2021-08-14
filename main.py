from backend.parameters import init_problem
from core.solver import ProblemSolver

l, w, h = 1, 1, 1
x1, y1, z1 = 0, 0.5, 0.5
x2, y2, z2 = 1, 1, 1
problem = init_problem(l, w, h, x1, y1, z1, x2, y2, z2)

if __name__ == '__main__':
    solver = ProblemSolver(problem)
    res = solver.solve()
    print("The solution to this problem is:", res)


