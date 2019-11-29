import enum
from main.main import *


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


    def find_area(self, start_point):
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
                if y1 > start_point.y:
                    par = par.right
                else:
                    par = par.left

        return par


    def local_area(self, root, old_area, new_areas, left_or_right):
        if root is None:
            return None
        if root.type == Type.Area and old_area.__eq__(root.key):
            self.update_tree(root, new_areas, left_or_right)
        self.local_area(root.left, old_area, new_areas, "left")
        self.local_area(root.right, old_area, new_areas, "right")


    def init_tree(self):
        a0,b0 = Point(0,0),Point(50,0)
        a1,b1 = Point(0,50),Point(50,50)
        line_b = Line(a0,b0)
        line_t = Line(a1,b1)
        start_area = Area(line_t,line_b, a0, b1)
        self.root = TreeNode(start_area, None, Type.Area)


    def build_tree(self, edges_list):
        self.init_tree()
        for e in edges_list:
            p = e.p1
            found_area = self.find_area(p)
            old_are, new_area = update_map(found_area, e)
            for area in old_are:
                self.local_area(self.root, area, new_area, 0)
        return self.root


    @staticmethod
    def update_tree(root, new_areas, left_or_right):
        parent = root.parent
        copy_root = root
        del root

        i = 0
        while i < 4 and new_areas[i].left_p[0] < copy_root.key.right_p[0]:
            i = i + 1

        if left_or_right == "left":

            if i == 4:
                    parent.left = TreeNode(new_areas[0].right_p, parent, Type.Point)

                    parent = parent.left

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
    c1 = Point(3,4)
    d1 = Point(9,8)
    line1 = Line(c1,d1)
    edges = [line1]
    roott = Tree().build_tree(edges)


main()









