
import math
import random

from sample_players import DataPlayer

class CustomPlayer(DataPlayer):
  """ Implement your own agent to play knight's Isolation

  The get_action() method is the only required method for this project.
  You can modify the interface for get_action by adding named parameters
  with default values, but the function MUST remain compatible with the
  default interface.

  **********************************************************************
  NOTES:
  - The test cases will NOT be run on a machine with GPU access, nor be
    suitable for using any other machine learning techniques.

  - You can pass state forward to your agent on the next turn by assigning
    any pickleable object to the self.context attribute.
  **********************************************************************
  """
  def get_action(self, state):
    """ Employ an adversarial search technique to choose an action
    available in the current state calls self.queue.put(ACTION) at least

    This method must call self.queue.put(ACTION) at least once, and may
    call it as many times as you want; the caller will be responsible for
    cutting off the function after the search time limit has expired.

    See RandomPlayer and GreedyPlayer in sample_players for more examples.

    **********************************************************************
    NOTE:
    - The caller is responsible for cutting off search, so calling
      get_action() from your own code will create an infinite loop!
      Refer to (and use!) the Isolation.play() function to run games.
    **********************************************************************
    """
    # TODO: Replace the example implementation below with your own search
    #       method by combining techniques from lecture
    #
    # EXAMPLE: choose a random move without any search--this function MUST
    #          call self.queue.put(ACTION) at least once before time expires
    #          (the timer is automatically managed for you)

    depth_limit = 100

    if state.ply_count < 2:
      self.queue.put(random.choice(state.actions()))
    else:
      for depth in range(1, depth_limit + 1):
        action = self.alpha_beta(state, depth)
        if action is not None:
          self.queue.put(action)

  def alpha_beta(self, state, depth):
    """Alpha beta pruning with iterative deepening"""
    beta = float("inf")
    best_score = float("-inf")
    best_move = None
    for a in state.actions():
        v = self.min_value(state.result(a), best_score, beta, depth - 1)
        if v > best_score:
            best_score = v
            best_move = a
    # writing depth and ply count info
    # DEBUG_INFO = open("depth,ply_count.txt", "a")
    # DEBUG_INFO.write(str(depth) + ", " + str(state.ply_count) + "\n")
    # DEBUG_INFO.close()
    return best_move

  def min_value(self, state, alpha, beta, depth):
    if depth <= 0:
      return self.custom_heuristics(state)
    if state.terminal_test():
      return state.utility(self.player_id)

    v = float("inf")
    for a in state.actions():
      v = min(v, self.max_value(state.result(a), alpha, beta, depth - 1))
      if v <= alpha:
        return v
      beta = min(beta, v)
    return v

  def max_value(self, state, alpha, beta, depth):
    if depth <= 0:
      return self.custom_heuristics(state)
    if state.terminal_test():
      return state.utility(self.player_id)

    v = float("-inf")
    for a in state.actions():
      v = max(v, self.min_value(state.result(a), alpha, beta, depth - 1))
      if v >= beta:
        return v
      alpha = max(alpha, v)
    return v

  def score(self, state):
    """
    own moves - opponent moves heuristic
    """
    own_loc = state.locs[self.player_id]
    opp_loc = state.locs[1 - self.player_id]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)
    return len(own_liberties) - len(opp_liberties)

  def custom_heuristics(self, state):
    """
    Linear combinations of features can be effective.
    Features for Isolation can include the ply, the distance between the player's tokens,
    distance from the edge (or center), and more (be creative).
    """
    own_loc = state.locs[self.player_id]
    opp_loc = state.locs[1 - self.player_id]
    player_distance = self.manhattan_distance(self.get_coordinates(own_loc), self.get_coordinates(opp_loc))
    own_moves_minus_opp_moves = self.score(state)

    if state.ply_count < 30:
      # chase the opponent for the first 30 moves
      return own_moves_minus_opp_moves - player_distance
    elif state.ply_count < 45:
      # move away from the opponent and the center (presumably using up corner space for moves) up to 45 moves
      return player_distance + own_moves_minus_opp_moves + self.distance_to_center(self.get_coordinates(own_loc))
    else:
      # endgame get close to the opponent and the center
      return 0 - player_distance + own_moves_minus_opp_moves - self.distance_to_center(self.get_coordinates(own_loc))

  def custom_heuristics_2(self, state):
    """
    Linear combinations of features can be effective.
    Features for Isolation can include the ply, the distance between the player's tokens,
    distance from the edge (or center), and more (be creative).
    """
    own_loc = state.locs[self.player_id]
    opp_loc = state.locs[1 - self.player_id]
    player_distance = self.manhattan_distance(self.get_coordinates(own_loc), self.get_coordinates(opp_loc))
    own_moves_minus_opp_moves = self.score(state)

    if state.ply_count < 30:
      # chase the opponent for the first 30 moves
      return own_moves_minus_opp_moves - player_distance
    elif state.ply_count < 50:
      # stay close to the opponent and the center up to 50 moves
      return 0 - player_distance + own_moves_minus_opp_moves + self.distance_to_center(self.get_coordinates(own_loc))
    else:
      # endgame - stay away from the oponent but still try to stay close to center
      # increace the effect of own_moves_minus_opp_moves value times 2 since
      # we'd like to keep its influence a bit higher in the endgame
      return player_distance + (own_moves_minus_opp_moves * 2) - self.distance_to_center(self.get_coordinates(own_loc))

  def own_moves(self, state):
    own_loc = state.locs[self.player_id]
    own_liberties = state.liberties(own_loc)
    return len(own_liberties)

  def get_coordinates(self, int_location):
    """
    Gets x,y coordinates out of an integer location
    """
    x = int_location % 13 # get column
    y = math.floor(int_location/13) # get row
    return x, y

  def distance_to_center(self, location):
    """
    Manhattan distance to center from given location
    """
    return self.manhattan_distance(location, (5, 4))

  def manhattan_distance(self, loc1, loc2):
    """
    Returns the manhattan distance between two points (loc1 and loc2)
    """
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])
