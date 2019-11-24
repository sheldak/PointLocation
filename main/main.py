class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = min(p1.x, p2.x)
        self.p2 = max(p1.x, p2.x)


class Area:
    def __init__(self, top_line, but_line, right_p, left_p):
        self.top_line = top_line
        self.but_line = but_line
        self.right_p = right_p
        self.left_p = left_p

        self.top_right = None
        self.but_right = None
        self.top_left = None
        self.but_left = None


class TrapezoidalMap:
    def __init(self):
        self.root = None
        self.top_right = None
        self.top_left = None
        self.but_left = None
        self.but_right = None

    def insert(self, area):
        if self.root is None:
            self.root = area
        else:
            add_right = self
            if area.but_line <= add_right.but_right.top_line:
                while add_right.but_right.right_p < area.left_p:
                    add_right = add_right.but_right
                prev = add_right.but_left
                prev.but_right = area
                area.but_right = add_right
            else:
                while add_right.top_right.right_p:
                    pass


def follow_segment(trapezoidal_map, search_structure, line):
    start_area = search_structure.find(p)

    j = 0
    areas = [start_area]

    while line.p2.x > areas[j].right_p:
        if areas[j].right_p.is_above(line):
            areas.append(areas[j].bottom_right)
        else:
            areas.append(areas[j].top_right)

        j += 1

    return areas


def update_map(trapezoidal_map, search_structure, line):
    areas = follow_segment(trapezoidal_map, search_structure, line)

    p = line.p1
    q = line.p2

    if len(areas) == 1:
        area_0 = areas[0]

        area_right = Area(area_0.top_line, area_0.bottom_line, area_0.right_p, q)
        area_top = Area(area_0.top_line, line, q, p)
        area_bottom = Area(line, area_0.bottom_line, q, p)

        area_0.right_p = p

        area_0.right

