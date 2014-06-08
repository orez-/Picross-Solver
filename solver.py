#!/usr/bin/python
# -*- coding: utf8 -*-


class Element(set):
    def __init__(self):
        set.__init__(self)
        self.value = None


def solve_board(horiz, vert):
    rows = [[Element() for _ in horiz] for _ in vert]
    cols = zip(*rows)
    annotated_rows = zip(vert, rows)
    annotated_cols = zip(horiz, cols)

    progress = True
    while progress:
        for lines, annotated_lines in ((rows, annotated_rows), (cols, annotated_cols)):
            for rule, line in annotated_lines:
                if not solve_line(line, rule):
                    raise Exception("Inconsistent board!!")

            progress = consolidate_board(rows)
            clear_board(rows)

    return rows


def consolidate_board(rows):
    progress = False
    for row in rows:
        for elem in row:
            if len(elem) == 1 and elem.value is None:
                elem.value = elem.pop()
                progress = True
    return progress


def clear_board(board):
    for row in board:
        for elem in row:
            elem.clear()


def solve_line(line, rule):
    if not rule:
        if any(e.value == 1 for e in line):  # if we didn't account for a dot
            return False
        for e in line:  # everything else is 'no'
            e.add(0)
        return True
    possible = False
    nr = rule[0]
    for i, first_elem in enumerate(line[: len(line) - nr + 1]):
        if (
            all(e.value in (1, None) for e in line[i: i + nr]) and
                (i + nr >= len(line) or line[i + nr].value in (0, None))):  # fits
            if solve_line(line[i + nr + 1:], rule[1:]):  # if the rest can be placed
                for e in line[: i]:  # everything before would be 'no'
                    e.add(0)
                for e in line[i: i + nr]:  # all of me would be 'yes'
                    e.add(1)
                if len(line) > i + nr:  # immediately following would be 'no'
                    line[i + nr].add(0)
                possible = True
        if first_elem.value == 1:  # this piece must use this square.
            break
    return possible


def str_board(board):
    lookup = {None: '.', 0: u'░', 1: u'▒'}
    return '\n'.join(''.join(lookup[elem.value] for elem in row) for row in board)


if __name__ == "__main__":
    # horiz = [(1, 1), (), (1, 1)]
    # vert = [(1, 1), (), (1, 1)]

    # horiz = [
    #    (2, 2), (1, 1, 2), (3, 2, 1), (6, ), (7, ), (7, ), (6, ), (3, 2, 1),
    #    (1, 1, 2), (2, 2)]
    # vert = [
    #    (1, 1), (1, 1, 1, 1), (1, 1, 2, 1, 1), (1, 4, 1), (6, ), (8, ), (1, 4, 1), (1, 6, 1),
    #    (1, 4, 1), (1, 1)]

    horiz = [
        (), (), (8,), (5, 2, 2), (6, 1, 2), (6, 5, 2, 1), (6, 1, 2, 3), (6, 1, 5),
        (4, 1, 2, 5), (1, 1, 1, 1), (1, 1, 1, 1), (4, 1, 2, 5), (6, 1, 5), (6, 1, 2, 3),
        (6, 5, 2, 1), (6, 1, 2), (5, 2, 2), (8,), (), ()]
    vert = [
        (6,), (4, 4), (5, 5), (6, 6), (6, 6), (6, 6), (5, 5), (3, 3), (1, 8, 1),
        (1, 1, 1, 1), (1, 1, 1, 1, 1, 1), (2, 1, 1, 1, 1, 2), (3, 3), (1, 2, 1),
        (1, 1), (10,), (2, 2, 2, 2), (1, 3, 3, 1), (1, 3, 3, 1), (1, 4, 4, 1)]

    board = solve_board(horiz, vert)
    print str_board(board)
