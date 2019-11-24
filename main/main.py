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