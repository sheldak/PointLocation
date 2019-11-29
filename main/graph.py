from sortedcontainers import SortedSet
import json


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def is_above(self, line):
        p2, p1 = max(line.p1, line.p2), min(line.p1, line.p2)

        a = (p2[1] - p1[1]) / (p2[0] - p1[0])  # współczynnik kierunkowy
        b = p1[1] - ((p2[1] - p1[1]) * p1[0]) / (p2[0] - p1[0])  # wyraz wolny

        return self.y > a*self.x + b


class Line:
    def __init__(self, p1, p2):
        if not isinstance(p1, Point):
            p1 = Point(p1[0], p1[1])

        if not isinstance(p2, Point):
            p2 = Point(p2[0], p2[1])

        self.p1 = min(p1, p2)
        self.p2 = max(p1, p2)

    def __hash__(self):
        return hash((self.p1, self.p2))

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def __lt__(self, other):
        return self.p1 < other.p1 or (self.p1 == other.p1 and self.p2 < other.p2)

    def print_line(self):
        print("[[{}, {}], [{}, {}]]".format(self.p1.x, self.p1.y, self.p2.x, self.p2.y))


class Polygon:
    def __init__(self, points):
        self.points = points
        self.lines = []
        self.make_lines()

    def make_lines(self):
        points = self.points
        lines = []

        for i in range(len(points)):
            lines.append(Line(points[i], points[(i+1) % len(points)]))

        self.lines = lines


class Area:
    def __init__(self, top_line, but_line, left_p, right_p):
        self.top_line = top_line
        self.but_line = but_line
        self.right_p = right_p
        self.left_p = left_p

        self.top_right = None
        self.but_right = None
        self.right = None

        self.top_left = None
        self.but_left = None
        self.left = None

    def __eq__(self, other):
        if not isinstance(other, Area):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.top_line == self.top_line and self.left_p == self.left_p and self.right_p == self.right_p and self.but_line == other.but_line


def make_polygons_from_json(file_name):
    polygons = []
    with open(file_name, 'r') as file:
        json_polygons = file.read()

    json_polygons = json.loads(json_polygons)

    for polygon in json_polygons:
        polygons.append(Polygon(polygon))

    return polygons


def make_lines_from_json(file_name):
    lines = []
    with open(file_name, 'r') as file:
        json_lines = file.read()

    json_lines = json.loads(json_lines)

    for line in json_lines:
        lines.append(Line(line[0], line[1]))

    return lines

def extract_all_lines(polygons):
    lines = SortedSet()
    for polygon in polygons:
        for line in polygon.lines:
            if line not in lines:
                lines.add(line)

    lines_list = []
    while lines:
        lines_list.append(lines.pop())

    return lines_list


def follow_segment(start_area, line):
    j = 0
    areas = [start_area]
    while line.p2.x > areas[j].right_p.x and j < 3:
        if areas[j].right_p.is_above(line):
            areas.append(areas[j].but_right)
        else:
            areas.append(areas[j].top_right)
        j += 1

    return areas


def update_map(start_area, line):
    old_areas = follow_segment(start_area, line)  # finding all areas crossed by the line
    new_areas = []  # areas which will override old areas

    p = line.p1  # start point of the line
    q = line.p2  # end point of the line

    top_area = Area(start_area.top_line, line, p, start_area.right_p)  # variable with current area above the line
    but_area = Area(line, start_area.but_line, p, start_area.right_p)  # variable with current area below the line

    if not start_area.left_p == p:  # when start of the line is not part of any other line
        left_area = Area(start_area.top_line, start_area.but_line, start_area.left_p, p)  # area on the left of line

        left_area.top_right = top_area  # connections from left area
        left_area.but_right = but_area

        top_area.left = left_area   # connections to left area
        but_area.left = left_area

        new_areas.append(left_area)  # adding area to the list

    for i in range(1, len(old_areas)-1):  # for every area crossed by the line
        if top_area.right_p.is_above(line):  # last old area has right_p above the line
            new_top_area = Area(old_areas[i].top_line, line,
                                old_areas[i].left_p, old_areas[i].right_p)  # new area on the right

            new_top_area.left = top_area  # connecting areas above the line
            top_area.right = new_top_area

            new_areas.append(top_area)  # adding last area to the list

            top_area = new_top_area  # now we are considering area on the right

            but_area.right_p = \
                old_areas[i].right_p  # changing right_p of the area below the line (that area will be bigger)

        else:  # last old area has right_p below the line
            new_but_area = Area(line, old_areas[i].but_line,
                                old_areas[i].left_p, old_areas[i].right_p)  # new area on the right

            new_but_area.left = but_area   # connecting areas below the line
            but_area.right = new_but_area

            new_areas.append(but_area)  # adding last area to the list

            but_area = new_but_area  # now we are considering area on the right

            top_area.right_p = \
                old_areas[i].right_p  # changing right_p of the area above the line (that area will be bigger)

    top_area.right_p = q  # right_p of both areas are the endpoint of the line
    but_area.right_p = q

    if not old_areas[len(old_areas)-1].right_p == q:  # when end of the line is not part of any other line
        right_area = Area(old_areas[len(old_areas)-1].top_line, old_areas[len(old_areas)-1].but_line,
                          q, old_areas[len(old_areas)-1].right_p)  # area on the right of the line

        right_area.top_left = top_area  # connections from right area
        right_area.but_left = but_area

        top_area.right = right_area  # connections to right area
        but_area.right = right_area

        new_areas.append(top_area)  # adding last 3 areas to the list
        new_areas.append(but_area)
        new_areas.append(right_area)
    else:
        new_areas.append(top_area)  # adding last 2 areas to the list
        new_areas.append(but_area)

    return old_areas, new_areas  # returning 2 lists


# all_polygons = make_polygons_from_json("../polygons/polygons_1.json")
#
# all_lines = extract_all_lines(all_polygons)
