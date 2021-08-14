

class Cuboid:

    def __init__(self, l, w, h):
        self.length = l
        self.width = w
        self.height = h

    def is_valid(self):
        length_ok = self.length > 0
        width_ok = self.width > 0
        height_ok = self.height > 0
        return length_ok & width_ok & height_ok

    def get_dimension(self):
        return self.length, self.width, self.height


class Point:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def is_valid(self, cuboid):

        if not cuboid.is_valid():
            return False

        length_ok = (self.x >= 0) & (self.x <= cuboid.length)
        width_ok = (self.y >= 0) & (self.y <= cuboid.width)
        height_ok = (self.z >= 0) & (self.z <= cuboid.height)

        if not length_ok & width_ok & height_ok:  # We prune this case
            return False

        is_on_wall1 = self.x in [0, cuboid.length]
        is_on_wall2 = self.y in [0, cuboid.width]
        is_on_wall3 = self.z in [0, cuboid.height]

        return is_on_wall1 | is_on_wall2 | is_on_wall3

    def get_coordinate(self):
        return self.x, self.y, self.z


class Problem:

    def __init__(self, room: Cuboid, lizard: Point, bug: Point):
        self.room = room
        self.lizard = lizard
        self.bug = bug

    def is_valid(self):
        return self.room.is_valid() & self.lizard.is_valid(self.room) & self.bug.is_valid(self.room)


def init_problem(l, w, h, x1, y1, z1, x2, y2, z2):
    room = Cuboid(l, w, h)
    bug = Point(x1, y1, z1)
    lizard = Point(x2, y2, z2)
    problem = Problem(room, lizard, bug)

    if problem.is_valid():
        return problem

    return
