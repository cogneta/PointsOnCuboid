import logging
import datetime as dt
import numpy as np
import os

from backend.parameters import Problem

logging.basicConfig(filename=os.path.dirname(os.path.dirname(__file__))
                             + f"/logs/log_{dt.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.txt",
                    level=logging.DEBUG,
                    format='SOLVER - %(levelname)s: %(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class ProblemSolver(Problem):

    def __init__(self, problem):
        super(ProblemSolver, self).__init__(problem.room, problem.lizard, problem.bug)

        self.same_x = bool()
        self.same_y = bool()
        self.same_z = bool()
        self.opposed_x = bool()
        self.opposed_y = bool()
        self.opposed_z = bool()

    def characterize(self):
        self.same_x = (self.lizard.x == self.bug.x) & (self.lizard.x in [0, self.room.length])
        self.same_y = (self.lizard.y == self.bug.y) & (self.lizard.y in [0, self.room.width])
        self.same_z = (self.lizard.z == self.bug.z) & (self.lizard.z in [0, self.room.height])

        self.opposed_x = abs(self.lizard.x - self.bug.x) == self.room.length
        self.opposed_y = abs(self.lizard.y - self.bug.y) == self.room.width
        self.opposed_z = abs(self.lizard.z - self.bug.z) == self.room.height

        same_wall = self.same_x | self.same_y | self.same_z

        opposed_wall = self.opposed_x | self.opposed_y | self.opposed_z

        if same_wall:
            return "same wall"
        elif opposed_wall:
            return "opposed wall"
        else:
            return "adjacent wall"

    def solve_same_wall(self):
        vec = np.array([self.lizard.x - self.bug.x,
                        self.lizard.y - self.bug.y,
                        self.lizard.z - self.bug.z])
        return np.linalg.norm(vec)

    def solve_opp_wall(self):
        l, w, h = self.room.get_dimension()
        x1, y1, z1 = self.lizard.get_coordinate()
        x2, y2, z2 = self.bug.get_coordinate()

        if self.opposed_y:
            x1, y1, z1 = y1, z1, x1
            x2, y2, z2 = y2, z2, x2
            l, w, h = w, h, l
        elif self.opposed_z:
            x1, y1, z1 = z1, x1, y1
            x2, y2, z2 = z2, x2, y2
            l, w, h = h, l, w

        if z1 + z2 > h:
            z1 = h - z1
            z2 = h - z2

        vec1 = np.array([y1 + l + y2, z1 - z2])
        vec2 = np.array([y1 + l + z2, z1 + y2])
        vec3 = np.array([y1 + l + (w - y2), z1 + w + z2])
        vec4 = np.array([y1 + l + y1, y1 + z2])
        vec5 = np.array([z1 + l + z2, y1 - y2])
        vec6 = np.array([z1 + l + (w - y2), (w - y1) + z2])
        vec7 = np.array([(w - y1) + l + y2, z1 + w + z2])
        vec8 = np.array([(w - y1) + l + z2, z1 + (w - y2)])
        vec9 = np.array([(w - y1) + l + (w - y2), z1 - z2])

        n1 = np.linalg.norm(vec1)
        n2 = np.linalg.norm(vec2)
        n3 = np.linalg.norm(vec3)
        n4 = np.linalg.norm(vec4)
        n5 = np.linalg.norm(vec5)
        n6 = np.linalg.norm(vec6)
        n7 = np.linalg.norm(vec7)
        n8 = np.linalg.norm(vec8)
        n9 = np.linalg.norm(vec9)

        logging.debug("{:.3f} / {:.3f} / {:.3f} / {:.3f} / {:.3f} / {:.3f} "
                      "/ {:.3f} / {:.3f} / {:.3f}".format(n1, n2, n3, n4, n5, n6, n7, n8, n9))
        return np.min((n1, n2, n3, n4, n5, n6, n7, n8, n9))

    def solve_adj_wall(self):

        l, w, h = self.room.get_dimension()
        x1, y1, z1 = self.lizard.get_coordinate()
        x2, y2, z2 = self.bug.get_coordinate()

        while not(x1 == 0 & y2 == 0):
            if x1 == l:
                x1 = l - x1
                x2 = l - x2
            elif z1 == 0:
                x1, y1, z1 = z1, y1, l - x1
                x2, y2, z2 = z2, y2, l - x2
                l, w, h = h, w, l
            elif z1 == h:
                x1, y1, z1 = h - z1, y1, z1
                x2, y2, z2 = h - z2, y2, z2
                l, w, h = h, w, l
            elif y1 == 0:
                x1, y1, z1 = y1, x1, z1
                x2, y2, z2 = y2, x2, z2
                l, w, h = w, l, h
            elif y1 == w:
                x1, y1, z1 = w - y1, x1, z1
                x2, y2, z2 = w - y2, x2, z2
                l, w, h = w, l, h
            else:
                x1, y1, z1 = x1, z1, w - y1
                x2, y2, z2 = x2, z2, w - y2
                l, w, h = l, h, w

        if z1 + z2 > h:
            z1 = h - z1
            z2 = h - z2

        vec1 = np.array([z1 + x2, y1 + z2])
        vec2 = np.array([y1 + x2, z1 - z2])

        n1 = np.linalg.norm(vec1)
        n2 = np.linalg.norm(vec2)

        logging.debug("{:.3f} / {:.3f}".format(n1, n2))
        return np.min((n1, n2))

    def solve(self):
        charact = self.characterize()
        logging.info(charact)
        if charact == "same wall":
            res = self.solve_same_wall()
        elif charact == "opposed wall":
            res = self.solve_opp_wall()
        elif charact == "adjacent wall":
            res = self.solve_adj_wall()
        else:
            logging.debug('wrong characterization output')
            raise ValueError('wrong characterization output')

        lb = np.linalg.norm(np.array([self.lizard.x - self.bug.x,
                                            self.lizard.y - self.bug.y,
                                            self.lizard.z - self.bug.z]))
        ub = self.room.length + self.room.width + self.room.height
        if (res >= lb) & (res <= ub):
            logging.debug('result = ' + str(res))
            return res
        else:
            logging.debug('result is not consistent with bounds, {:.3f} not in [{:.3f}, {:.3f}]'.format(res, lb, ub))
            return
