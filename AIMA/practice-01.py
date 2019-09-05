# practice-01.py
# Inteligencia Artificial, tercer curso del Grado de Ingeniería Informática -
# Grupo en Inglés. Universidad de Sevilla.

# Practice 1: Search
# ====================

# On this practice we will work with a Python implementation of the main
# search algorithms discussed in class. We will check their behaviour on
# the 8-puzzle problem (also seen in class). The practice consists on
# three well-differentiated parts:

# Part I: Representation of problems as state spaces. A general technique will
# be shown, and will be implemented for the particular case of the 8-puzzle.

# Part II: Implementation of search algorithms for state spaces.
# Some general search patterns will be shown, and how the algorithms seen
# in class are particular cases of such general patterns.

# Part III: Experimentation with the implemented algorithms. By running the
# algorithms to find solutions of the 8-puzzle, some of its properties will
# be noticed.


# The code of this practice is mostly taken from the python code supplied with
# the book "Artificial Intelligence: A Modern Approach" by S. Russell & P. Norvig
# (http://code.google.com/p/aima-python, module search.py). The code has been
# edited (also adapting it to Python 3) by José Luis Ruiz Reina 
# (Dpt. de Ciencias de la Computación e Inteligencia Artificial.
# Universidad de Sevilla).



# This is needed for the Emacs python-mode, who does not update correctly
# the load path for modules. If you're not using Emacs, remove this.
# If you're using Emacs, edit and write the absolute path where this file is
# (and the auxiliary queues.py)
import sys
sys.path.append("/home/agustin/Escritorio/13oct2012/practice-01")


# We will need the following module "queues" provided along with this file:
from queues import *


#===================================================
# PART I. REPRESENTATION OF PROBLEMS AS STATE SPACES
#===================================================



# Recall that, as seen in class, the implementation of a representation
# of a problem as a state consists on:

# * Represent states and actions using some data structure.
# * Define: initial_state, is_final_state(_), actions(_), apply(_,_) and
#   cost_of_applying_action, if the problem has an associated cost.

# The following class "Problem" represents this general scheme for any
# state space problem. A particular problem will be a subclass of
# Problem, which will require to implement actions, apply, and eventually __init__,
# is_final_state y  cost_of_applying_action. 


class Problem(object):
    """Abstract class for state space problems. For particular problems
    specific subclasses of Problem will be defined, implementing
    actions, apply and eventually __init__, is_final_state and
    cost_of_applying_action. Once defined, it is necessary to create
    instances of such subclass, which will be given as input to the
    search algorithms for solving the problem."""  


    def __init__(self, initial_state, final_state=None):
        """The constructor of the specific class of the initial state, and
        maybe also for the final state, if it is unique. The subclasses could
        add further arguments"""
        
        self.initial_state = initial_state
        self.final_state = final_state

    def actions(self, state):
        """Returns the applicable actions to a given state. Normally
        a list could be obtained, but if there are too many it might
        be more efficient to return an iterator."""
        abstract

    def apply(self, state, action):
        """Returns the state obtained after applying the action on the state.
        The action is supposed to be applicable on the state (that is, it must be
        one of the actions from self.actions(state)."""
        abstract

    def is_final_state(self, state):
        """Returns True when the state is final. By default, compares against
        the final state, if it has been specified upon construction. If we
        deal with a problem where no final state is given (there is a checking
        function istead), or there are several final states, then this method
        must be redefined in the subclass."""
        return state == self.final_state

    def cost_of_applying_action(self, state, action):
        """Returns the cost of applying the action on the state.
         By default, this cost is 1. Reimplement if the problem sets
         a different cost function.""" 
        return 1

# Below there is an example on how to define a problem as a subclass
# of Problem. More pecisely, the water jug problem, seen in class,
# but having slightly different actions:

class Jugs(Problem):
    """The water jug problem:
    States will be represented as tuples (x,y) of two integers,
    where x is the number of liters of the 4-liter and y is the number of liters
    of the 3-liter jug."""

    def __init__(self):
        super().__init__((0,0))

    def actions(self,state):
        jug_4=state[0]
        jug_3=state[1]
        acts=list()
        if jug_4 > 0:
            acts.append("empty the 4-liter jug")
            if jug_3 < 3:
                acts.append("pour from the 4-liter jug into the 3-liter jug")
        if jug_4 < 4:
            acts.append("fill the 4-liter jug")
            if jug_3 > 0:
                acts.append("pour from the 3-liter jug into the 4-liter jug")
        if jug_3 > 0:
            acts.append("empty the 3-liter jug")
        if jug_3 < 3:
            acts.append("fill the 3-liter jug")
        return acts

    def apply(self,state,action):
        j4=state[0]
        j3=state[1]
        if action=="fill the 4-liter jug":
            return (4,j3)
        elif action=="fill the 3-liter jug":
            return (j4,3)
        elif action=="empty the 4-liter jug":
            return (0,j3)
        elif action=="empty the 3-liter jug":
            return (j4,0)
        elif action=="pour from the 4-liter jug into the 3-liter jug":
            return (j4-3+j3,3) if j3+j4 >= 3 else (0,j3+j4)
        else: #  "pour from the 3-liter jug into the 4-liter jug"
            return (j3+j4,0) if j3+j4 <= 4 else (4,j3-4+j4)

    def is_final_state(self,state):
        return state[0]==2


# Examples:

# >>> pj = Jugs()
# >>> pj.initial_state
# (0, 0)
# >>> pj.actions(pj.initial_state)
# ['fill the 4-liter jug', 'fill the 3-liter jug']
# >>> pj.apply(pj.initial_state,"fill the 4-liter jug")
# (4, 0)
# >>> pj.cost_of_applying_action(pj.initial_state,"fill the 4-liter jug")
# 1
# >>> pj.is_final_state(pj.initial_state)
# False

    
    
# ------------
# Exercise 1
# -----------    

# ---------------------------------------------------------------------------
# Define the class Eight_Puzzle, that implements the representation of the
# 8-puzzle problem seen in class. To this aim, fill in the slots marked
# with ????? on the code below.
# ----------------------------------------------------------------------------


# class Eight_Puzzle(Problem):
#     """Problem of the 8-puzzle.  States will be implemented as tuples of
#     9 elements, permutations of numbers from 0 to 8 (0 is the blank space).
#     This represents the location of the tiles on the board, reading rows
#     up to down, and within a row, from left to right. For example, the
#     final state is the tuple (1, 2, 3, 8, 0, 4, 7, 6, 5). The four
#     actions of the problem will be represented as the strings:
#     "move space up", "move space down", "move space left" y
#     "move space right", respectively. 
#     """"

#     def __init__(self,initial_board):
#         super().__init__(initial_state=?????, final_state=?????)

#     def actions(self,state):
#         pos_space=state.index(0)
#         acts=list()
#         if pos_space not in ?????: 
#             acts.append(?????)
#         if pos_space not in ?????: 
#             acts.append(?????)
#         if pos_space not in ?????: 
#             acts.append(?????)
#         if pos_space not in ?????: 
#             acts.append(?????)
#         return acts     

#     def apply(self,state,action):
#         ???????

# Examples that can be executed after defining the class:

# >>> p8p_1 = Eight_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# >>> p8p_1.initial_state
# (2, 8, 3, 1, 6, 4, 7, 0, 5)
# >>> p8p_1.final_state
# (1, 2, 3, 8, 0, 4, 7, 6, 5)
# >>> p8p_1.actions(p8p_1.initial_state)
# ['move space up', 'move space left', 'move space right']
# >>> p8p_1.apply(p8p_1.initial_state,"move space up")
# (2, 8, 3, 1, 0, 4, 7, 6, 5)
# >>> p8p_1.cost_of_applying_action(p8p_1.initial_state,"move space up")
# 1

# ----------------------------------------------------------------------------





















#==============================================================
# PART II. IMPLEMENTATION OF SEARCH ALGORITHMS FOR STATE SPACES
#==============================================================

# In this part we shall implement the algorithms of Breadth-first-search,
# Depth-first-search, Optimal-search, Best-first-search, and
# A-star-search. The first two will be stated as particular cases of the
# so-called General-search (as seen in class) and the remaining three
# will be particular cases of Search_with_priority (that is, a search
# where the queue is sorted according to some given value).

# -----------
# Exercise 2
# -----------

# ---------------------------------------------------------------------------
# Recall from the lectures that nodes of the search trees are different
# from the state space nodes. A search tree node must contain the
# following information:
#     - The state
#     - A pointer to the previous state (parent)
#     - The last action that was applied (to the parent) in order to
#       obtain the node's state
#     - Depth of the node
#     - Cost of the path from the initial state to the node's state.





# Define the class Node, implementing the nodes of a search tree.
# To this aim, fill in the slots marked with ????? on the code below.

# ----------------------------------------------------------------------------

# class Node:
#     """Nodes of a search tree. A node is defined as:
#       - The state
#       - A pointer to the previous state (parent)
#       - The last action that was applied (to the parent) in order to
#         obtain the node's state
#       - Depth of the node
#       - Cost of the path from the initial state to the node's state.
       
#        Besides,we define, among others, the following methods that will
#        be used when generating the search tree: 
#        - Successor and successors of a node (by one action, or by all
#          actions applicable on the node's state, resp.) 
#        - Path (sequence of nodes) starting from the initial node.
#        - Solution (sequence of actions that lead to the node's state).   
#        """

#     def __init__(self, state, parent=None, action=None, path_cost=0):
#         self.state=state
#         self.parent=parent
#         self.action=action
#         self.path_cost=path_cost
#         self.depth=0
#         if parent: 
#             self.depth= self.depth + 1

#     def __repr__(self):
#         return "<Node {0}>".format(self.state)

#     def successor(self, problem, action):
#         """Successor of a node by an applicable action"""
#         ?????


#     def successors(self, problem):
#         """List of successor nodes by all applicable actions""" 
#         ?????

#     def path(self):
#         """List of nodes connecting the initial node to the
#            node.""" 
#         ?????

#     def solution(self):
#         """Sequence de actions starting from the initial node"""
#         ?????

#     def __eq__(self, other):
#         """ Two nodes are the same if their states are the same. This
#         means that when checking membership on a list or a set (using "in"),
#         we just look at states. If, for example, we need to look at
#         the cost, then we will have to do it explicitly, like for
#         search_with_priority"""
        
#         return isinstance(other, Node) and self.state == other.state

#     def __lt__(self, other): 
#         """Defining the less-than relation between nodes is needed because
#         when introducing a node in the priority queue having the same value
#         as an already existing one, nodes will be compared and hence we need
#         the operator < to be defined"""  
#         return True
    
#     def __hash__(self):
#         """Note that this definition imposes that states must be of
#         a hashable data type"""
#         return hash(self.state)  
                                  
# -----------------------------------------------------------------------------

# Example that can be executed after defining the class:
#
# >>> p8p_1 = Eight_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# >>> np8p_1=(Node(p8p_1.initial_state))
# >>> np8p_1.successors(p8p_1)
# [<Node (2, 8, 3, 1, 0, 4, 7, 6, 5)>, <Node (2, 8, 3, 1, 6, 4, 0, 7, 5)>, 
#   <Node (2, 8, 3, 1, 6, 4, 7, 5, 0)>]

# ----------------------------------------------------------------------------























                                  
# -----------
# Exercise 3
# -----------

# Implement the general search, as explained in class. 
# To this aim, fill in the slots marked with ????? on the code below.
# In this implementation the closed list is a set of states (type set)
# and the open list (frontier) is a queue of nodes.

# def general_search(problem, frontier):
#     """General search, as explained in class; here
#     frontier is a queue that can be handled in several ways. 
#     When the function is called, the argument frontier must be the
#     empty queue. 
#     Keep in mind that in this search, when checking if a node is repeated
#     we just look at the state. Hence, searches using cost (optimal or
#     A*, for example), cannot be obtained as particular cases of this one
#     (they will be particular cases of search_with_priority"""


#     frontier.append(Node(problem.initial_state))
#     closed = set()
#     while frontier:
#         actual = ?????  
#         if ?????:
#             return actual
#         closed.add(?????)
#         new_successors= ?????
#         ?????
#     return None



# The frontier queue is received as an argument and it will be an instance
# of one of the queue types defined in the module queues.py. Keep in mind
# that in such module, for every type of queue,the methods
# pop(), append(_) and extend(_) are supported, removing the first element
# of the queue, or adding an element, or a list of elements to the queue,
# respectively. The management of the queue will be something internal
# to the queue object itself.

# ------------------------------------------------------------------------------













# -----------
# Exercise 4
# -----------

# Using general search, implement the algorithms breadth_first_search
# and depth_first_search.
# Hint: Initiate frontier as a LIFO or FIFO queue, respectively. 

# Examples of usage:

# >>> breadth_first_search(Jugs()).solution()
# ['fill the 4-liter jug', 'pour from the 4-liter jug into the 3-liter jug', 
#  'empty the 3-liter jug', 'pour from the 4-liter jug into the 3-liter jug', 
#  'fill the 4-liter jug', 'pour from the 4-liter jug into the 3-liter jug']
# >>> depth_first_search(Jugs()).solution()
# ['fill the 3-liter jug', 'pour from the 3-liter jug into the 4-liter jug', 
#  'fill the 3-liter jug', 'pour from the 3-liter jug into the 4-liter jug', 
#  'empty the 4-liter jug', 'pour from the 3-liter jug into the 4-liter jug']
# >>> breadth_first_search(Eight_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))).solution()
# ['move space up', 'move space up', 'move space left', 
#  'move space down', 'move space right']
# >>> depth_first_search(Eight_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))).solution()
# ['move space right', 'move space up', ... ] # more than 3000 actions!


# ------------------------------------------------------------------------------
















# ------------------------------------------------------------------------------



# ----------------------------------------------------------------

# The following function search_with_priority(problem,f), defines a
# general search where frontier is handled as a queue with
# priority, sorting the nodes from lower to greater values of f.
# Note that best-first search, optimal search and A* search
# can be seen as particular cases of this search, using
# different "f"s.

# This search with priority differs from the general search of
# exercise 3 in the following: if one of the generated nodes has the same
# state as a node in frontier but the new node has a lower cost, then it
# has to be included in frontier.

def search_with_priority(problem, f):
    """Search where the frontier queue is handled by sorting nodes by
    increasing values of f. Note that best-first search,
    optimal search, and A* search are particular cases of this search,
    using different f's (heuristic, cost, and cost plus heuristic,
    respectively)."""
    
    actual = Node(problem.initial_state)
    if problem.is_final_state(actual.state):
        return actual
    frontier = QueuePriority(min, f)
    frontier.append(actual)
    closed = set()
    while frontier:
        actual = frontier.pop()
        if problem.is_final_state(actual.state):
            return actual
        closed.add(actual.state)
        for successor in actual.successors(problem):
            if successor.state not in closed and successor not in frontier:
                frontier.append(successor)
            elif successor in frontier:
                node_with_same_state = frontier[successor]
                if f(successor) < f(node_with_same_state): 
                    del frontier[node_with_same_state]
                    frontier.append(successor)
    return None



# -----------
# Exercise 5
# -----------

# Using the previously defined search_with_priority, implement the
# algorithms for optimal_search, best_first_search and
# a_star_search. Note that the two last algorithms get as input
# not only the problem, but also the heuristic function to be used.


# ------------------------------------------------------------------------------




















# ------------------------------------------------------------------------------

#===============================================
# PART III. EXPERIMENTATION
#===============================================


# -----------
# Exercise 6
# -----------


# Define the two heuristic functions for the 8-puzzle discussed in
# class. That is:
# - h1_eight_puzzle(state): counts the number of pieces out of their
#   correct positions (w.r.t. final state).
# - h2_eight_puzzle_state(state): sum of the Manhattan distances of
#   each tile to its position in the final state.

# Examples:

# >>> h1_eight_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# 4
# >>> h2_eight_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# 5
# >>> h1_eight_puzzle((5,2,3,0,4,8,7,6,1))
# 4
# >>> h2_eight_puzzle((5,2,3,0,4,8,7,6,1))
# 11


# Fill in the slots marked with ????? on the code below.

# def h1_eight_puzzle(state):
#     """Counts number of misplaced tiles"""
#     cont=0
#     for x,y in ???????:
#         if x !=0 and x!=y: cont += 1
#     return cont        



# def h2_eight_puzzle(state): 
#     """Sum of Manhattan distances of each tile to
#        its position in final state"""
    
#     positions_final=(4,0,1,2,5,8,7,6,3) # positions_final[i] is the position
#                                         # of i in the final state  
#     sum= 0                                                            
#     for i in range(9):
#         statei=state[i]
#         if statei != 0:
#             j=?????                     # j is the position at final state
#                                         # of the tile at position i in state
#             i_x,i_y=i//3,i%3
#             j_x,j_y=j//3,j%3
#             sum += ?????
#     return sum


# ------------------------------------------------------------------------------

















# ------------------------------------------------------------------------------

#============
# Exercise 7
#============

# Find a solution using optimal_search, best_first_search and
# a_star_search (trying each of the two heuristics), the 8-puzzle problem
# for the following initial state:

#              +---+---+---+
#              | 2 | 8 | 3 |
#              +---+---+---+
#              | 1 | 6 | 4 |
#              +---+---+---+
#              | 7 | H | 5 |
#              +---+---+---+
# ------------------------------------------------------------------------------

























# ------------------------------------------------------------------------------
# The following definitions will allow us to run experiments using
# different initial states, algorithms and heuristics, in order to solve
# the 8-puzzle. Besides, the number of nodes analyzed during the search
# will be counted:


class Problem_with_Analyzed(Problem):

    """It's a problem identical to the one received when it is
       initialized, only adding up a new attribute to store the
       number of nodes analyzed during the search. In this way,
       we do not need to modify the code of the search algorithms.""" 
         
    def __init__(self, problem):
        self.initial_state = problem.initial_state
        self.problem = problem
        self.analyzed  = 0

    def actions(self, state):
        return self.problem.actions(state)

    def apply(self, state, action):
        return self.problem.apply(state, action)

    def is_final_state(self, state):
        self.analyzed += 1
        return self.problem.is_final_state(state)

    def cost_of_applying_action(self, state, action):
        return self.problem.cost_of_applying_action(state,action)



def solve_eight_puzzle(initial_state, algorithm, h=None):
    """Function that applies a given search algorithm to the eight-puzzle
       problem, with a given initial state and (if required by the algorithm)
       a given heuristic.
       Example of usage:

       >>> solve_eight_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5),a_star_search,h2_eight_puzzle)
       Solution: ['move space up', 'move space up', 'move space left', 
                  'move space down', 'move space right']
       Algorithm: a_star_search
       Heuristic: h2_eight_puzzle
       Length of the solution: 5. Nodes analyzed: 7
       """

    p8p=Problem_with_Analyzed(Eight_Puzzle(initial_state))
    sol= (algorithm(p8p,h).solution() if h else algorithm(p8p).solution()) 
    print("Solution: {0}".format(sol))
    print("Algorithm: {0}".format(algorithm.__name__))
    if h: 
        print("Heuristic: {0}".format(h.__name__))
    else:
        pass
    print("Length of the solution: {0}. Nodes analyzed: {1}".format(len(sol),p8p.analyzed))


#============
# Exercise 8
#============

# Try to solve using the different search algorithms and, if it is the case,
# the different heuristics, the 8-puzzle problem for the following
# initial states (you may also try your own further examples):

#           E1              E2              E3              E4
#           
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+    
#     | 2 | 8 | 3 |   | 4 | 8 | 1 |   | 2 | 1 | 6 |   | 5 | 2 | 3 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
#     | 1 | 6 | 4 |   | 3 | H | 2 |   | 4 | H | 8 |   | H | 4 | 8 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
#     | 7 | H | 5 |   | 7 | 6 | 5 |   | 7 | 5 | 3 |   | 7 | 6 | 1 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
    
# For each case, you should use the function solve_eight_puzzle, in order
# to obtain, not only the solution, but also its length (cost) and
# the number of nodes analyzed. Write the results on the following
# table (L="length of the solution", NA="nodes analyzed"), and
# explain them according to the theoretical properties studied.


#                                       E1           E2           E3          E4
                                
# Breadth-First                       L=            L=           L=          L=  
#                                     NA=           NA=          NA=         NA= 
                                                                              
# Depth-First                         L=            L=           L=          L=  
#                                     NA=           NA=          NA=         NA= 
                                                                              
# Optimal                             L=            L=           L=          L=  
#                                     NA=           NA=          NA=         NA= 
                                                                              
# Best-First (h1)                     L=            L=           L=          L=
#                                     NA=           NA=          NA=         NA=
                                                                              
# Best-First (h2)                     L=            L=           L=          L= 
#                                     NA=           NA=          NA=         NA=
                                                                              
# A* (h1)                             L=            L=           L=          L= 
#                                     NA=           NA=          NA=         NA=
                                                                              
# A* (h2)                             L=            L=           L=          L= 
#                                     NA=           NA=          NA=         NA=

# -----------------------------------------------------------------------------------------


















#---------------------------------------------------------------------------



#============
# Exercise 9
#============

# The following heuristic h3_eight_puzzle is obtained by adding to heuristic
# h2_eight_puzzle a component that accounts for the "sequentiality" in the
# cells of the board, when reading them clockwise.
# Is h3 admissible? Check how this heuristic behaves when used for
# A*, on each of the previous states. Comment the results.


def h3_eight_puzzle(state):

    suc_eight_puzzle ={0: 1, 1: 2, 2: 5, 3: 0, 4: 4, 5: 8, 6: 3, 7: 6, 8: 7}  

    def sequentiality_aux(state,i):
        
        val=state[i]
        if val == 0:
            return 0
        elif i == 4:
            return 1
        else:
            i_sig=suc_eight_puzzle[i]
            val_sig = (val+1 if val<8 else 1)
            return 0 if val_sig == state[i_sig] else 2 

    def sequentiality(state):
        res= 0 
        for i in range(8): 
            res+=sequentiality_aux(state,i)
        return res    

    return h2_eight_puzzle(state) + 3*sequentiality(state)
                   

# ---------------------------------------------------------------------------

