import solver


def format_input(heading, line_separator='\t', entry_separator=' '):
    return [
        [int(num) for num in line.split(entry_separator) if num and int(num)]
        for line in heading.split(line_separator)]


if __name__ == "__main__":
    horiz = format_input(raw_input("Horizontal: "))
    vert = format_input(raw_input("Vertical  : "))
    board = solver.solve_board(horiz, vert)
    print solver.str_board(board)
