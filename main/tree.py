


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
        self.arr = dict()

    def find_area(self, line):
        start_point = line.p1

        if self.root is None:
            return None
        par = self.root
        while par.type != Type.Area:
            if par.type == Type.Point:
                if par.key.x > start_point.x:
                    par = par.left
                else:
                    par = par.right
            elif par.type == Type.Line:
                x1, y1 = par.key.p1.x, par.key.p1.y
                x2, y2 = par.key.p2.y, par.key.p2.y
                if y1 > start_point.y:
                    par = par.right
                elif y1 < start_point.y:
                    par = par.left
                else:  # the same y
                    par_slope = (y2 - y1) / (x2 - x1)
                    line_slope = (line.p2.y - line.p1.y) / (line.p2.x - line.p1.x)
                    if par_slope >= line_slope:
                        par = par.left
                    else:
                        par = par.right

        return par

    def local_area(self, root, old_area, new_areas, left_or_right):
        if root is None:
            return None
        if root.type == Type.Area and old_area.__eq__(root.key):
            #print(root.type)
            self.update_tree(root, new_areas, left_or_right)
        self.local_area(root.left, old_area, new_areas, "left")
        self.local_area(root.right, old_area, new_areas, "right")

    def print_tree(self, root):
        if root is None:
            return
        self.print_tree(root.left)
        if root.type == Type.Point:
            print("Punkt", root.key.x,  root.key.y)
        elif root.type == Type.Line:
            print("Linia", root.key.p1.x, root.key.p1.y, root.key.p2.x, root.key.p2.y)
        else:
            print("Obszar", root.key.left_p.x,  root.key.left_p.y,  root.key.right_p.x, root.key.right_p.y)
        self.print_tree(root.right)

    def init_tree(self):
        a0, b0 = Point(0, 0), Point(400, 0)  # TODO make it automatical
        a1, b1 = Point(0, 400), Point(400, 400)
        line_b = Line(a0, b0)
        line_t = Line(a1, b1)
        start_area = Area(line_t, line_b, a0, b1)
        self.root = TreeNode(start_area, None, Type.Area)

    def first_step(self, new_areas):
        root = TreeNode(new_areas[0].right_p, None, Type.Point)

        root.left = TreeNode(new_areas[0], root, Type.Area)
        self.arr[(new_areas[0].left_p, new_areas[0].right_p, new_areas[0].top_line, new_areas[0].but_line)] = root.left
        root.right = TreeNode(new_areas[0].top_right.right_p, root, Type.Point)

        parent = root.right

        parent.right = TreeNode(new_areas[3], parent, Type.Area)
        self.arr[(new_areas[3].left_p, new_areas[3].right_p, new_areas[3].top_line, new_areas[3].but_line)] = parent.right
        parent.left = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)

        parent = parent.left

        parent.left = TreeNode(new_areas[0].top_right, parent, Type.Area)
        self.arr[(new_areas[0].top_right.left_p, new_areas[0].top_right.right_p, new_areas[0].top_right.top_line, new_areas[0].top_right.but_line)] = parent.left
        parent.right = TreeNode(new_areas[0].but_right, parent, Type.Area)
        self.arr[(new_areas[0].but_right.left_p, new_areas[0].but_right.right_p, new_areas[0].but_right.top_line, new_areas[0].but_right.but_line)] = parent.right

        del self.root
        self.root = root

    def build_tree(self, edges_list):
        self.init_tree()
        old_areas, new_areas = update_map(self.root.key, edges_list[0])
        self.first_step(new_areas)

        for i in range(1, len(edges_list)):
            e = edges_list[i]
            found_area = self.find_area(e)
            old_areas, new_areas = update_map(found_area.key, e)
            for area in old_areas:
                self.local_area(self.root, area, new_areas, "left")
        return self

    def add_lead(self, parent, area, left_or_right):
        if self.arr.get((area.left_p, area.right_p, area.top_line, area.but_line)) is None:
            if left_or_right == "left":
                parent.left = TreeNode(area, parent, Type.Area)
                self.arr[(area.left_p, area.right_p, area.top_line, area.but_line)] = parent.left
            else:
                parent.right = TreeNode(area, parent, Type.Area)
                self.arr[(area.left_p, area.right_p, area.top_line, area.but_line)] = parent.right
        else:
            if left_or_right == "left":
                parent.left = self.arr[(area.left_p, area.right_p, area.top_line, area.but_line)]
            else:
                parent.right = self.arr[(area.left_p, area.right_p, area.top_line, area.but_line)]

    def update_tree(self, root, new_areas, left_or_right):
        parent = root.parent
        copy_root = root
        del root
        i = 0

        for j in range(0, len(new_areas)):

            if i == 4:
                break
            if new_areas[j].left_p.x >= copy_root.key.right_p.x:
                break
            if new_areas[j].right_p.x > copy_root.key.left_p.x:
                i = i + 1

        print(i)

        if left_or_right == "left":
            if i == 4:
                parent.left = TreeNode(new_areas[0].right_p, parent, Type.Point)
                parent = parent.left

                self.add_lead(parent, new_areas[0], "left")
                parent.right = TreeNode(new_areas[0].top_right.right_p, parent, Type.Point)
                parent = parent.right

                self.add_lead(parent, new_areas[3], "right")
                parent.left = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)
                parent = parent.left

                self.add_lead(parent, new_areas[0].top_right, "left")
                self.add_lead(parent, new_areas[0].but_right, "right")

            elif i == 3:
                parent.left = TreeNode(new_areas[0].right_p, parent, Type.Point)
                parent = parent.left
                if new_areas[0].left_p == copy_root.key.left_p:
                    print("Lewy sie styka")
                    self.add_lead(parent, new_areas[2], "right")
                    parent.left = TreeNode(new_areas[0].but_line, parent, Type.Line)
                    parent = parent.left

                    self.add_lead(parent, new_areas[2].top_left, "left")
                    self.add_lead(parent, new_areas[2].but_left, "right")
                    #parent.left = TreeNode(new_areas[2].top_left, parent, Type.Area)
                    #parent.right = TreeNode(new_areas[2].but_left, parent, Type.Area)

                elif new_areas[0].but_right.top_line.p1 == copy_root.key.right_p:
                    print("Prawy sie styka")
                    self.add_lead(parent, new_areas[0], "left")
                    #parent.left = TreeNode(new_areas[0], parent, Type.Area)
                    parent.right = TreeNode(new_areas[0].but_right.top_line, parent, Type.Line)
                    parent = parent.right

                    self.add_lead(parent, new_areas[0].top_right, "left")
                    self.add_lead(parent, new_areas[0].but_right, "right")
                    #parent.left = TreeNode(new_areas[0].top_right, parent, Type.Area)
                    #parent.right = TreeNode(new_areas[0].but_right, parent, Type.Area)

                else:
                    if new_areas[0].left_p.x >= copy_root.key.left_p.x:
                        print("Zaczyna na koncu")
                        self.add_lead(parent, new_areas[0], "left")
                        #parent.left = TreeNode(new_areas[0], parent, Type.Area)
                        parent.right = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)
                        parent = parent.right
                    else:
                        print("Zaczyna na poczatku")
                        print("LEFt")
                        parent.left = TreeNode(new_areas[0].but_line, parent, Type.Line)
                        parent.right = TreeNode(new_areas[2], parent, Type.Area)
                        parent = parent.left

                    self.add_lead(parent, new_areas[2].top_left, "left")
                    self.add_lead(parent, new_areas[2].but_left, "right")
                    #parent.left = TreeNode(new_areas[0].top_right, parent, Type.Area)
                    #parent.right = TreeNode(new_areas[0].but_right, parent, Type.Area)
                del new_areas[0]
                del new_areas[0]

            elif i == 2:
                parent.left = TreeNode(new_areas[0].but_line, parent, Type.Line)
                parent = parent.left

                self.add_lead(parent, new_areas[0], "left")
                #parent.left = TreeNode(new_areas[0], parent, Type.Area)
                self.add_lead(parent, new_areas[1], "right")
                parent.right = TreeNode(new_areas[1], parent, Type.Area)

        elif left_or_right == "right":
            if i == 4:
                parent.right = TreeNode(new_areas[0].right_p, parent, Type.Point)
                parent = parent.right

                self.add_lead(parent, new_areas[0], "left")
                #parent.left = TreeNode(new_areas[0], parent, Type.Area)
                parent.right = TreeNode(new_areas[0].top_right.right_p, parent, Type.Point)
                parent = parent.right

                self.add_lead(parent, new_areas[3], "right")
                #parent.right = TreeNode(new_areas[3], parent, Type.Area)
                parent.left = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)
                parent = parent.left

                self.add_lead(parent, new_areas[0].top_right, "left")
                self.add_lead(parent, new_areas[0].but_right, "right")
                #parent.left = TreeNode(new_areas[0].top_right, parent, Type.Area)
                #parent.right = TreeNode(new_areas[0].but_right, parent, Type.Area)

            elif i == 3:
                parent.right = TreeNode(new_areas[0].right_p, parent, Type.Point)
                parent = parent.right
                if new_areas[0].left_p == copy_root.key.left_p:
                    print("Lewy sie styka")
                    self.add_lead(parent, new_areas[2], "right")
                    #parent.right = TreeNode(new_areas[2], parent, Type.Area)
                    parent.left = TreeNode(new_areas[0].but_line, parent, Type.Line)
                    parent = parent.left

                    self.add_lead(parent, new_areas[2].top_left, "left")
                    self.add_lead(parent, new_areas[2].but_left, "right")
                    #parent.left = TreeNode(new_areas[2].top_left, parent, Type.Area)
                    #parent.right = TreeNode(new_areas[2].but_left, parent, Type.Area)

                elif new_areas[0].but_right.top_line.p1 == copy_root.key.right_p:
                    print("Prawy sie styka")
                    self.add_lead(parent, new_areas[0], "left")
                    #parent.left = TreeNode(new_areas[0], parent, Type.Area)
                    parent.right = TreeNode(new_areas[0].but_right.top_line, parent, Type.Line)
                    parent = parent.right

                    self.add_lead(parent, new_areas[0].top_right, "left")
                    self.add_lead(parent, new_areas[0].but_right, "right")
                    #parent.left = TreeNode(new_areas[0].top_right, parent, Type.Area)
                    #parent.right = TreeNode(new_areas[0].but_right, parent, Type.Area)

                else:
                    if new_areas[0].left_p.x >= copy_root.key.left_p.x:
                        print("Zaczyna na koncu")
                        print("prawy")
                        self.add_lead(parent, new_areas[0], "left")
                        #parent.left = TreeNode(new_areas[0], parent, Type.Area)
                        parent.right = TreeNode(new_areas[0].top_right.but_line, parent, Type.Line)
                        parent = parent.right
                    else:
                        print("Zaczyna na poczatku")
                        print("prawy")
                        parent.left = TreeNode(new_areas[0].but_line, parent, Type.Line)
                        self.add_lead(parent, new_areas[2], "right")
                        #parent.right = TreeNode(new_areas[2], parent, Type.Area)
                        parent = parent.left
                    new_areas[2].pr
                    self.add_lead(parent, new_areas[2].top_left, "left")
                    self.add_lead(parent, new_areas[2].but_left, "right")
                    #parent.left = TreeNode(new_areas[0].top_right, parent, Type.Area)
                    #parent.right = TreeNode(new_areas[0].but_right, parent, Type.Area)
                    del new_areas[0]
                    del new_areas[0]

            elif i == 2:
                parent.right = TreeNode(new_areas[0].but_line, parent, Type.Line)
                parent = parent.right

                self.add_lead(parent, new_areas[0], "left")
                self.add_lead(parent, new_areas[1], "right")
                #parent.left = TreeNode(new_areas[0], parent, Type.Area)
                #parent.right = TreeNode(new_areas[1], parent, Type.Area)



def main():
    # all_polygons = make_polygons_from_json("/polygons/polygons_1.json")
    # all_lines = extract_all_lines(all_polygons)
    all_lines = make_lines_from_json("polygons/polygons_1.json")
    # TODO randomize lines

    roott = Tree().build_tree(all_lines)
    roott.print_tree(roott.root)
    print(roott.find_area(Line(Point(50, 100), Point(150, 200))).key.right_p.x)


main()