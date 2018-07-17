
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

    if state.ply_count < 2:
      self.queue.put(random.choice(state.actions()))
    else:
      self.uct_search(state)

# Monte Carlo Tree Search
  def uct_search(self, state):
    v0 = Node(state)
    while True:
      v1 = self.tree_policy(v0)
      delta = self.default_policy(v1.state)
      self.backup(v1, delta)
      best = self.best_child(v0, 0) # get the child with the max avg score (since c == 0)
      best_action = None
      # get the action that results in that best child
      for action in v0.state.actions():
        if v0.state.result(action) == best.state:
          best_action = action
      self.queue.put(best_action)
  
  # choosing a node for expansion
  def tree_policy(self, v):
    while not v.state.terminal_test():
        # if v not fully expanded - there are more actions from the node state than children nodes)
      if len(v.state.actions()) > len(v.children):
        return self.expand(v)
      else:
        v = self.best_child(v, 1/math.sqrt(2))
    return v

  def expand(self, v):
    # choose a random untried action
    action = random.choice([a for a in v.state.actions() if a not in [child.action for child in v.children]])
    v1 = Node(v.state.result(action))
    v.add_child(v1, action)
    return v1

  def best_child(self, v, c):
    return max(v.children, key=lambda x: (x.Q / x.N) + (c * math.sqrt(2 * math.log(v.N) / x.N)))

  # rollout
  def default_policy(self, state):
    player_id = state.player() # active player at the start of the simulation
    while not state.terminal_test():
      action = random.choice(state.actions())
      state = state.result(action)
    return 1 if state.utility(player_id) < 0 else -1
    # the default policy should return +1 if the agent holding initiative 
    # at the start of a simulation loses 
    # and -1 if the active agent when the simulation starts wins 
    # because nodes store the reward relative to their parent in the game tree.

  def backup(self, v, delta):
    while v is not None:
      v.N += 1
      v.Q += delta
      delta = -delta
      v = v.parent


class Node():
  def __init__(self, state):
    self.state = state
    self.children = []
    self.parent = None
    self.action = None
    self.N = 0
    self.Q = 0

  def add_child(self, child, action):
    self.children.append(child)
    child.action = action
    child.parent = self

  def add_parent(self, state):
    v = Node(state)
    self.parent = v