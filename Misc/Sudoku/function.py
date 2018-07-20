from utils import *

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
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
