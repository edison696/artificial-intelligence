
from sample_players import DataPlayer

class CustomPlayer(DataPlayer):
  """ Implement your own agent to play knight's Isolation

  The get_action() method is the only *required* method. You can modify
  the interface for get_action by adding named parameters with default
  values, but the function MUST remain compatible with the default
  interface.

  **********************************************************************
  NOTES:
  - You should **ONLY** call methods defined on your agent class during
    search; do **NOT** add or call functions outside the player class.
    The isolation library wraps each method of this class to interrupt
    search when the time limit expires, but the wrapper only affects
    methods defined on this class.

  - The test cases will NOT be run on a machine with GPU access, nor be
    suitable for using any other machine learning techniques.
  **********************************************************************
  """
  def get_action(self, state):
      """ Employ an adversarial search technique to choose an action
      available in the current state calls self.queue.put(ACTION) at least

      This method must call self.queue.put(ACTION) at least once, and may
      call it as many times as you want; the caller is responsible for
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

      depth_limit = 20

      for depth in range(1, depth_limit + 1):
        action = self.alpha_beta(state, depth)
        self.queue.put(action)
        DEBUG_INFO = open("depth_ply_action.txt", "a")
        DEBUG_INFO.write("added action to queue " + str(action) + "\n")
        DEBUG_INFO.write("***********************************\n")
        DEBUG_INFO.close()

  def alpha_beta(self, state, depth):
    """Alpha beta pruning with iterative deepening"""
    
    alpha = float("-inf")
    beta = float("inf")
    best_score = float("-inf")
    best_move = None
    for a in state.actions():
        v = self.min_value(state.result(a), alpha, beta, depth - 1)
        alpha = max(alpha, v)
        if v > best_score:
            best_score = v
            best_move = a
    # open a file for writing debug info
    DEBUG_INFO = open("depth_ply_action.txt", "a")
    DEBUG_INFO.write("board state " + "Isolation(board=" + str(state.board) + ", ply_count=" + str(state.ply_count) + ", locs=" + str(state.locs) + ")\n")
    DEBUG_INFO.write("depth " + str(depth) + "\n")
    DEBUG_INFO.write("ply count " + str(state.ply_count) + "\n")
    DEBUG_INFO.write("best move " + str(best_move) + "\n")
    DEBUG_INFO.write("----------------------------------\n")
    DEBUG_INFO.close()
    return best_move

  def min_value(self, state, alpha, beta, depth):
    if state.terminal_test():
      return state.utility(self.player_id)
    if depth <= 0:
      return self.score(state)

    v = float("inf")
    for a in state.actions():
      v = min(v, self.max_value(state.result(a), alpha, beta, depth - 1))
      if v <= alpha:
        return v
      beta = min(beta, v)
    return v

  def max_value(self, state, alpha, beta, depth):
    if state.terminal_test():
      return state.utility(self.player_id)
    if depth <= 0:
      return self.score(state)
    
    v = float("-inf")
    for a in state.actions():
      v = max(v, self.min_value(state.result(a), alpha, beta, depth - 1))
      if v >= beta:
        return v
      alpha = max(alpha, v)
    return v
  
  def score(self, state):
    # # own moves - opponent moves heuristic
    own_loc = state.locs[self.player_id]
    opp_loc = state.locs[1 - self.player_id]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)
    return len(own_liberties) - len(opp_liberties)

    # own moves heuristic
    # loc = state.locs[self.player_id]
    # return len(state.liberties(loc))