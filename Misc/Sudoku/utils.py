rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
# Element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top most row.
column_units = [cross(rows, c) for c in cols]
# Element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# Element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top left square.
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

unitlist = row_units + column_units + square_units

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for key, value in values.items():
        if len(value) == 1:
            # eliminate values

            # in the same row
            for x in row_units[rows.find(key[0])]:
                if len(values[x]) > 1:
                    values[x] = values[x].replace(value, '')

            # in the same column
            for x in column_units[cols.find(key[1])]:
                if len(values[x]) > 1:
                    values[x] = values[x].replace(value, '')

            # in the same square
            for square_unit in square_units:
                if key in square_unit:
                    for x in square_unit:
                        if len(values[x]) > 1:
                            values[x] = values[x].replace(value, '')
    return values

    #Udacity solution
    # solved_values = [box for box in values.keys() if len(values[box]) == 1]
    # for box in solved_values:
    #     digit = values[box]
    #     for peer in peers[box]:
    #         values[peer] = values[peer].replace(digit,'')
    # return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    unsolved_boxes = sorted([box for box in values.keys() if len(values[box]) > 1])
    for box in unsolved_boxes:
        digits = values[box]
        # check each digit
        for digit in digits:

            # check row peers
            row_occurence = 0
            for x in row_units[rows.find(box[0])]:
                if values[x].find(digit) != -1:
                    row_occurence += 1
            if row_occurence == 1: # only choice for the row
                values[box] = digit
                break

            # check column peers
            column_occurence = 0
            for x in column_units[cols.find(box[1])]:
                if values[x].find(digit) != -1:
                    column_occurence += 1
            if column_occurence == 1: # only choice for the column
                values[box] = digit
                break

            # check square peers
            square_occurence = 0
            for square_unit in square_units:
                if box in square_unit:
                    for x in square_unit:
                        if values[x].find(digit) != -1:
                            square_occurence += 1
            if square_occurence == 1: # only choice for the square
                values[box] = digit
                break

    return values
    # Udacity solution
    # for unit in unitlist:
    #     for digit in '123456789':
    #         dplaces = [box for box in unit if digit in values[box]]
    #         if len(dplaces) == 1:
    #             values[dplaces[0]] = digit
    # return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    # not sure what the line above does, it wasn't in the original solution?
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
