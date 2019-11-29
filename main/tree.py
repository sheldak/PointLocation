import enum
from main.graph import *
# from PointLocation.main.main import *


class Type(enum.Enum):
    Point = 0
    Line = 1
    Area = 2


class TreeNode:
    def __init__(self, key, parent, type):
        self.key = key
        self.left = None
        self.right = None
        self.type = type
        self.parent = parent


class Tree:
    def __init__(self):
        self.root = None


    def find_area(self, line):
        start_point = line.p1

        if self.root is None:
            return None
        par = self.root
        while par.type != Type.Area:
            if par.Type == Type.Point:
                if par.key.x > start_point.x:
                    par = par.left
                else:
                    par = par.right
            elif par.Type == Type.Line:
                (x1, y1) = par.key.p1
                (x2, y2) = par.key.p2
                if y1 > start_point.y:
                    par = par.right
                elif y1 < start_point.y:
                    par = par.left
                else:  # the same y
                    par_slope = (y2 - y1) / (x2 - x1)
                    line_slope = (line.p2.y - line.p1.y) / (line.p2.x - line.p1.x)
                    if par_slope > line_slope:
                        par = par.left
                    else:
                        par = par.right

        return par


    def local_area(self, root, old_area, new_areas, left_or_right):
        if root is None:
            return None
        if root.type == Type.Area and old_area.__eq__(root.key):
            self.update_tree(root, new_areas, left_or_right)
        self.local_area(root.left, old_area, new_areas, "left")
        self.local_area(root.right, old_area, new_areas, "right")


    def print_tree(self, root):
        if root is None:
            return None
        print(root.key)
        self.print_tree(root.left)
        self.print_tree(root.right)

    def init_tree(self):
        a0,b0 = Point(0,0),Point(400,0) # TODO make it automatical
        a1,b1 = Point(0,400),Point(400,400)
        line_b = Line(a0,b0)
        line_t = Line(a1,b1)
        start_area = Area(line_t,line_b, a0, b1)
        self.root = TreeNode(start_area, None, Type.Area)


    def build_tree(self, edges_list):
        self.init_tree()
        for e in edges_list:
            found_area = self.find_area(e)
            old_areas, new_areas = update_map(found_area.key, e)
            for area in old_areas:
                self.local_area(self.root, area, new_areas, "left")
        return self


    def update_tree(self, root, new_areas, left_or_right):
        parent = root.parent
        copy_root = root
        isNone = False

        if root.parent is not None:
            print(root.parent)
            del root

        if root.parent is None:
            isNone = True

        i = 0
        while i < 4 and new_areas[i].left_p.x < copy_root.key.right_p.x:
            i = i + 1

        if left_or_right == "left":

            if i == 4:
                    parent.left = TreeNode(new_areas[0].right_p, parent, Type.Point)

                    if isNone:
                        self.root = parent.left

                    parent = parent.left

                    if isNone:
                        del root

                    parent.left = TreeNode(new_areas[0], parent, Type.Area)
                    parent.right = TreeNode(new_areas[0].top_right.right_p, parent, Type.Point)

                    parent = parent.right

                    parent.right = TreeNode(new_areas[3], parent, Type.Area)
                    parent.left = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)

                    parent = parent.left

                    parent.left = TreeNode(new_areas[0].top_right, parent, Type.Area)
                    parent.right = TreeNode(new_areas[0].but_right, parent, Type.Area)



            elif i == 3:
                if new_areas[0].left_p.y != copy_root.key.left_p.y and new_areas[0].right_p.y != copy_root.key.right_p.y :  # nie stykają się

                    parent.left = TreeNode(new_areas[0].right_p, parent, Type.Point)

                    parent = parent.left

                    if new_areas[0].left_p.x < copy_root.key.right_p.x and new_areas[0].right_p.x < copy_root.key.right_p.x :
                        parent.left = TreeNode(new_areas[0], parent, Type.Area)
                        parent.right = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)

                        parent = parent.right

                    elif new_areas[2].left_p.x >= copy_root.key.right_p.x  :
                        parent.left = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)
                        parent.right = TreeNode(new_areas[2], parent, Type.Point)

                        parent = parent.left

                    parent.left = TreeNode(new_areas[0].top_right, parent, Type.Area)
                    parent.right = TreeNode(new_areas[0].but_right, parent, Type.Area)

            else:
                if new_areas[0].left_p.y != copy_root.key.left_p.y and new_areas[0].right_p.y != copy_root.key.right_p.y:

                    parent.left = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)

                    parent = parent.left

                    parent.left = TreeNode(new_areas[0].top_right, parent, Type.Area)
                    parent.right = TreeNode(new_areas[0].but_right, parent, Type.Area)


        elif left_or_right == "right":

            if i == 4:
                    parent.right = TreeNode(new_areas[0].right_p, parent, Type.Point)

                    parent = parent.right

                    parent.left = TreeNode(new_areas[0], parent, Type.Area)
                    parent.right = TreeNode(new_areas[0].top_right.right_p, parent, Type.Point)

                    parent = parent.right

                    parent.right = TreeNode(new_areas[3], parent, Type.Area)
                    parent.left = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)

                    parent = parent.left

                    parent.left = TreeNode(new_areas[0].top_right, parent, Type.Area)
                    parent.right = TreeNode(new_areas[0].but_right, parent, Type.Area)

            elif i == 3:
                if new_areas[0].left_p.y != copy_root.key.left_p.y and new_areas[0].right_p.y != copy_root.key.right_p.y:  # nie stykają się

                    parent.right = TreeNode(new_areas[0].right_p, parent, Type.Point)

                    parent = parent.right
                    if new_areas[0].left_p.x < copy_root.key.right_p and new_areas[0].right_p.x < copy_root.key.right_p.x:
                        parent.left = TreeNode(new_areas[0], parent, Type.Area)
                        parent.right = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)

                        parent = parent.right

                    elif new_areas[2].left_p.x >= copy_root.key.right_p.x  :
                        parent.left = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)
                        parent.right = TreeNode(new_areas[2], parent, Type.Point)

                        parent = parent.left

                    parent.left = TreeNode(new_areas[0].top_right, parent, Type.Area)
                    parent.right = TreeNode(new_areas[0].but_right, parent, Type.Area)

            else:
                if new_areas[0].left_p.y != copy_root.key.left_p.y and new_areas[0].right_p.y != copy_root.key.right_p.y:
                    parent.right = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)

                    parent = parent.right

                    parent.left = TreeNode(new_areas[0].but_right, parent, Type.Area)
                    parent.right = TreeNode(new_areas[0].top_right, parent, Type.Area)

        while i > 0 :
            del new_areas[0]
            i = i - 1



def main():
    # all_polygons = make_polygons_from_json("../polygons/polygons_1.json")
    # all_lines = extract_all_lines(all_polygons)
    all_lines = make_lines_from_json("../polygons/lines_1.json")
    # TODO randomize lines

    roott = Tree().build_tree(all_lines)
    roott.print_tree(roott.root)
    print(roott.find_area(Line(Point(200, 200), Point(200,200))).key.right_p.x)


main()









