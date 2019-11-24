class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = min(p1.x, p2.x)
        self.p2 = max(p1.x, p2.x)


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


# class TrapezoidalMap:
#     def __init__(self):
#         self.root = None
#         self.top_right = None
#         self.top_left = None
#         self.but_left = None
#         self.but_right = None
#
#     def insert(self, area):
#         if self.root is None:
#             self.root = area
#         else:
#             add_right = self
#             if area.but_line <= add_right.but_right.top_line:
#                 while add_right.but_right.right_p < area.left_p:
#                     add_right = add_right.but_right
#                 prev = add_right.but_left
#                 prev.but_right = area
#                 area.but_right = add_right
#             else:
#                 while add_right.top_right.right_p:
#                     pass


def follow_segment(search_structure, line):
    start_area = search_structure.find(line.p1)

    j = 0
    areas = [start_area]

    while line.p2.x > areas[j].right_p:
        if areas[j].right_p.is_above(line):
            areas.append(areas[j].but_right)
        else:
            areas.append(areas[j].top_right)

        j += 1

    return areas


def update_map(trapezoidal_map, search_structure, line):
    areas = follow_segment(search_structure, line)

    p = line.p1
    q = line.p2

    # if len(areas) == 1:
    #     area_0 = areas[0]
    #
    #     area_right = Area(area_0.top_line, area_0.but_line, q, area_0.right_p)
    #     area_top = Area(area_0.top_line, line, p, q)
    #     area_but = Area(line, area_0.but_line, p, q)
    #
    #     area_0.right_p = p
    #
    #     area_0.top_right = area_top
    #     area_0.but_line = area_but
    #
    #     area_top.left = area_0
    #     area_top.right = area_right
    #
    #     area_but.left = area_0
    #     area_but.right = area_right
    #
    #     area_right.top_left = area_top
    #     area_right.but_left = area_but
    #     area_right.right = area_0.right
    #
    # else:

    top_area = Area(areas[0].top_line, line, line.p1, areas[0].top_line.p2)
    but_area = Area(line, areas[0].but_line, line.p1, areas[0].but_line.p2)

    top_area.left = areas[0]
    but_area.left = areas[0]

    if start_with_point(line):
        top_area.left = None
        but_area.left = None
    else:
        areas[0].top_right = top_area
        areas[0].but_right = but_area

    for i in range(1, len(areas)):
        if areas[i].left_p.is_above(line):
            curr_top_area = Area(areas[i].to_line, line, areas[i].left_p, areas[i].right_p)
            but_area.right_p = areas[i].right_p




