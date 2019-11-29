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

    def __eq__(self, other):
        if not isinstance(other, Area):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.top_line == self.top_line and self.left_p == self.left_p and self.right_p == self.right_p and self.but_line == other.but_line


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


def follow_segment(start_area, line):
    j = 0
    areas = [start_area]

    while line.p2.x > areas[j].right_p:
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
