
from utils import *


row_units = [cross(r, cols) for r in rows]
# Element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top most row.
column_units = [cross(rows, c) for c in cols]
# Element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top left square.
diagonal_units = [[rs + cs for (rs, cs) in zip(rows, cols)], 
                    [rs + cs for (rs, cs) in zip(rows, reversed(cols))]]
# diagonal_units[0] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
# diagonal_units[1] = ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist + diagonal_units


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # TODO: Implement this function!
    naked_twins_list = []
    for unit in unitlist:
        # list of tuples(box1, box2, value)
        # where box1 and box2 have the same value of length 2
        add_to_list = [(box1,box2,values[box1]) for box1 in unit for box2 in unit if box1 != box2 and len(values[box1]) == 2 and values[box1] == values[box2]]
        if len(add_to_list) > 0:
            naked_twins_list.extend(add_to_list)
        
    for naked_twin in naked_twins_list:
        affected_units = [unit for unit in unitlist if naked_twin[0] in unit and naked_twin[1] in unit]
        for affected_unit in affected_units:
            for box in affected_unit:
                if box != naked_twin[0] and box != naked_twin[1]:
                    for digit in naked_twin[2]:
                        values[box] = values[box].replace(digit, '')

    # # Udacity reviewer suggested algorithm improvement
    # # get a list of all boxes with 2 digits (2 possible values)
    # twin_values = [box for box in values.keys() if len(values[box]) == 2]
    # for box in twin_values:
    #     twin = values[box]
    #     twin_units = units[box] # what's units[box]?

    #     for u in twin_units:
    #         tplaces = [p for p in u if twin == values[p]]
    #         if len(tplaces) > 1:
    #             for peer in u:
    #                 if values[peer] != twin:
    #                     for d in twin:
    #                         values[peer] = values[peer].replace(d, '')



    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    # Added diagonal units
    # for key, value in values.items():
    #     if len(value) == 1:
    #         # eliminate values

    #         # in the same row
    #         for x in row_units[rows.find(key[0])]:
    #             if len(values[x]) > 1:
    #                 values[x] = values[x].replace(value, '')

    #         # in the same column
    #         for x in column_units[cols.find(key[1])]:
    #             if len(values[x]) > 1:
    #                 values[x] = values[x].replace(value, '')

    #         # in the same square
    #         for square_unit in square_units:
    #             if key in square_unit:
    #                 for x in square_unit:
    #                     if len(values[x]) > 1:
    #                         values[x] = values[x].replace(value, '')
            
    #         # in the same diagonal
    #         for diagonal_unit in diagonal_units:
    #             if key in diagonal_unit:
    #                 for x in diagonal_unit:
    #                     if len(values[x]) > 1:
    #                         values[x] = values[x].replace(value, '')
    # return values

    #Udacity solution
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    # Added diagonal units
    # unsolved_boxes = sorted([box for box in values.keys() if len(values[box]) > 1])
    # for box in unsolved_boxes:
    #     digits = values[box]
    #     # check each digit
    #     for digit in digits:

    #         # check row peers
    #         row_occurence = 0
    #         for x in row_units[rows.find(box[0])]:
    #             if values[x].find(digit) != -1:
    #                 row_occurence += 1
    #         if row_occurence == 1: # only choice for the row
    #             values[box] = digit
    #             break

    #         # check column peers
    #         column_occurence = 0
    #         for x in column_units[cols.find(box[1])]:
    #             if values[x].find(digit) != -1:
    #                 column_occurence += 1
    #         if column_occurence == 1: # only choice for the column
    #             values[box] = digit
    #             break

    #         # check square peers
    #         square_occurence = 0
    #         for square_unit in square_units:
    #             if box in square_unit:
    #                 for x in square_unit:
    #                     if values[x].find(digit) != -1:
    #                         square_occurence += 1
    #         if square_occurence == 1: # only choice for the square
    #             values[box] = digit
    #             break

    #         # check diagonal peers
    #         diagonal_occurence = 0
    #         for diagonal_unit in diagonal_units:
    #             if box in diagonal_unit:
    #                 for x in diagonal_unit:
    #                     if values[x].find(digit) != -1:
    #                         diagonal_occurence += 1
    #         if diagonal_occurence == 1: # only choice for the square
    #             values[box] = digit
    #             break

    # return values
    # Udacity solution
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    # Added naked tweens call
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Your code here: Use the Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier

    # Choose one of the unfilled squares with the fewest possibilities
    min_value = 9
    min_key = None
    for box in values:
        if len(values[box]) < min_value and len(values[box]) > 1:
            min_value = len(values[box])
            min_key = box

    if min_key is None:
        return values ## solved!

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    len_box_values = len(values[min_key])
    for i in range (len_box_values):
        new_sudoku = values.copy()
        new_sudoku[min_key] = values[min_key][i]
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    # If you're stuck, see the solution.py tab!

    # Udacity solution
    # "Using depth-first search and propagation, try all possible values."
    # # First, reduce the puzzle using the previous function
    # values = reduce_puzzle(values)
    # if values is False:
    #     return False ## Failed earlier
    # if all(len(values[s]) == 1 for s in boxes):
    #     return values ## Solved!
    # # Choose one of the unfilled squares with the fewest possibilities
    # n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # # Now use recurrence to solve each one of the resulting sudokus, and
    # for value in values[s]:
    #     new_sudoku = values.copy()
    #     new_sudoku[s] = value
    #     attempt = search(new_sudoku)
    #     if attempt:
    #         return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
