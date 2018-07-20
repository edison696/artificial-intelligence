# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start: {}".format(problem.getStartState()))
    print("Is the start a goal? {}".format(problem.isGoalState(problem.getStartState())))
    print("Start's successors: {}".format(problem.getSuccessors(problem.getStartState())))
    """
    "*** YOUR CODE HERE ***"

    # Return None if the start state is also the goal state
    # Don't need to move at all
    if problem.isGoalState(problem.getStartState()):
        return None

    explored = set()
    explored.add(problem.getStartState())
    frontier = util.Stack()
    for action in problem.getSuccessors(problem.getStartState()):
        frontier.push([action])
    # while not frontier.isEmpty():
    #     print(frontier.pop())
    # [((4, 5), 'West', 1)]
    # [((5, 4), 'South', 1)]
    
    while True:
        if frontier.isEmpty():
            return False
        path = frontier.pop()
        state = path[-1][0]
        explored.add(state)
        if problem.isGoalState(state):
            actions = [x[1] for x in path]
            return actions

        for action in problem.getSuccessors(state):
            result_state = action[0]
            if result_state not in explored:
                new_path = list(path)
                new_path.append(action)
                frontier.push(new_path)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Return None if the start state is also the goal state
    # Don't need to move at all
    if problem.isGoalState(problem.getStartState()):
        return None

    explored = set()
    explored.add(problem.getStartState())
    frontier = util.Queue()
    frontier_set = set()
    for action in problem.getSuccessors(problem.getStartState()):
        frontier.push([action])
        frontier_set.add(action[0])
    # while not frontier.isEmpty():
    #     print(frontier.pop())
    # [((4, 5), 'West', 1)]
    # [((5, 4), 'South', 1)]
    
    while True:
        if frontier.isEmpty():
            return False
        path = frontier.pop()
        state = path[-1][0]
        explored.add(state)
        if problem.isGoalState(state):
            actions = [x[1] for x in path]
            return actions

        for action in problem.getSuccessors(state):
            result_state = action[0]
            if result_state not in explored.union(frontier_set):
                new_path = list(path)
                new_path.append(action)
                frontier.push(new_path)
                frontier_set.add(result_state)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Return None if the start state is also the goal state
    # Don't need to move at all
    if problem.isGoalState(problem.getStartState()):
        return None

    explored = set()
    explored.add(problem.getStartState())
    frontier = util.PriorityQueue()
    frontier_set = set()
    for action in problem.getSuccessors(problem.getStartState()):
        frontier.push([action], action[2])
        frontier_set.add(action[0])
    # while not frontier.isEmpty():
    #     print(frontier.pop())
    # [((4, 5), 'West', 1)]
    # [((5, 4), 'South', 1)]
    
    while True:
        if frontier.isEmpty():
            return False
        path = frontier.pop()
        state = path[-1][0]
        explored.add(state)
        if problem.isGoalState(state):
            actions = [x[1] for x in path]
            return actions

        for action in problem.getSuccessors(state):
            result_state = action[0]
            if (result_state not in explored.union(frontier_set) or
                    problem.isGoalState(result_state)):
                new_path = list(path)
                new_path.append(action)
                # calculate new_path cost before adding path to frontier
                new_path_cost = 0
                for new_path_action in new_path:
                    new_path_cost += new_path_action[2]
                frontier.push(new_path, new_path_cost)
                frontier_set.add(result_state)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Return None if the start state is also the goal state
    # Don't need to move at all
    if problem.isGoalState(problem.getStartState()):
        return None

    explored = set()
    explored.add(problem.getStartState())
    frontier = util.PriorityQueue()
    frontier_set = set()
    for action in problem.getSuccessors(problem.getStartState()):
        frontier.push([action], action[2] + heuristic(action[0], problem))
        frontier_set.add(action[0])
    # while not frontier.isEmpty():
    #     print(frontier.pop())
    # [((4, 5), 'West', 1)]
    # [((5, 4), 'South', 1)]
    
    while True:
        if frontier.isEmpty():
            return False
        path = frontier.pop()
        state = path[-1][0]
        explored.add(state)
        if problem.isGoalState(state):
            actions = [x[1] for x in path]
            return actions

        for action in problem.getSuccessors(state):
            result_state = action[0]
            if (result_state not in explored.union(frontier_set) or
                    problem.isGoalState(result_state)):
                new_path = list(path)
                new_path.append(action)
                # calculate new_path cost before adding path to frontier
                new_path_cost = 0
                for new_path_action in new_path:
                    new_path_cost += new_path_action[2]
                # add the cost + the heuristic as the priority when 
                # pushing the path on the frontier
                frontier.push(
                    new_path, 
                    new_path_cost + heuristic(result_state, problem)
                )
                frontier_set.add(result_state)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
