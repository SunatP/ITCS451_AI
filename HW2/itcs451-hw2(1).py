"""A module for homework 2. Version 2."""
# noqa: D413

import abc
import copy
import heapq
import itertools
from collections import defaultdict
from typing import List, Any

from hw1 import EightPuzzleState, EightPuzzleNode


def eightPuzzleH1(state: EightPuzzleState, goal_state: EightPuzzleState):
    # for count misplaced tiles
    # for i in range(len(goal_board)):
    #     for j in range(len(goal_board)):
    #         if goal_board[i][j] != goal_board[i][j]:
    #             sum += 1
    sum = 0
    goal_board = goal_state.board
    for x in range(len(goal_board)):
        for y in range(len(goal_board[0])):
            if goal_board[x][y] != goal_board[x][y]:
                sum += 1
    return sum

    """
    Return the number of misplaced tiles including blank.

    Parameters
    ----------
    state : EightPuzzleState
        an 8-puzzle state containing a board (List[List[int]])
    goal_state : EightPuzzleState
        a desired 8-puzzle state.

    Returns
    ----------
    int

    """
    # TODO 1:


def eightPuzzleH2(state: EightPuzzleState, goal_state: EightPuzzleState):
    sum = 0
    # for i in range(0,3,1):
    #     for j in range(0,3,1):
    #         bij = b[i][j]
    #         i_b = i
    #         j_b = j

    #         i_g,j_g = value_index(g,bij)
    #         sum += (math.fabs(i_g - i_b) + math.fabs(j_g - j_b))
    goal_board = goal_state.board
    for i in range(len(goal_board)):
        for j in range(len(goal_board[0])):
            tile = goal_board[i][j]
            for m in range(len(goal_board)):
                for n in range(len(goal_board)):
                    if tile == goal_board[m][n]:
                        sum += abs(i - m) + abs(j + n)

    return sum
    """
    Return the total Manhattan distance from goal position of all tiles.

    Parameters
    ----------
    state : EightPuzzleState
        an 8-puzzle state containing a board (List[List[int]])
    goal_state : EightPuzzleState
        a desired 8-puzzle state.

    Returns
    ----------
    int

    """
    # TODO 2:


class Frontier(abc.ABC):
    """An abstract class of a frontier."""

    def __init__(self):
        """Create a frontier."""
        raise NotImplementedError()

    @abc.abstractmethod
    def is_empty(self):
        """Return True if empty."""
        raise NotImplementedError()

    @abc.abstractmethod
    def add(self, node):
        """
        Add a node into the frontier.

        Parameters
        ----------
        node : EightPuzzleNode

        Returns
        ----------
        None

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def next(self):
        """
        Return a node from a frontier and remove it.

        Returns
        ----------
        EightPuzzleNode

        Raises
        ----------
        IndexError
            if the frontier is empty.

        """
        raise NotImplementedError()


class DFSFrontier(Frontier):
    """An example of how to implement a depth-first frontier (stack)."""

    def __init__(self):
        """Create a frontier."""
        self.stack = []

    def is_empty(self):
        """Return True if empty."""
        return len(self.stack) == 0

    def add(self, node):
        """
        Add a node into the frontier.

        Parameters
        ----------
        node : EightPuzzleNode

        Returns
        ----------
        None

        """
        for i in self.stack:
            if i.state == node.state:
                return None
        self.stack.append(node)

    def next(self):
        """
        Return a node from a frontier and remove it.

        Returns
        ----------
        EightPuzzleNode

        Raises
        ----------
        IndexError
            if the frontier is empty.

        """
        return self.stack.pop()


class GreedyFrontier(Frontier):
    """A frontier for greedy search."""

    def __init__(self, h_func, goal_state):
        """
        Create a frontier.

        Parameters
        ----------
        h_func : callable h(state)
            a heuristic function to score a state.


        """
        self.goal = goal_state
        self.h = h_func
        self.queue = []
        self.find = {}
        self.count = itertools.count()

    pass

    def is_empty(self):
        return len(self.queue) == 0

    def add(self, node: EightPuzzleNode):
        if node in self.find:
            self.rem(node)
        count = next(self.count)

        priority = self.h(node.state, self.goal)
        entry = [priority, count, node]
        self.find[node] = entry
        heapq.heappush(self.queue, entry)
        pass

    def next(self):
        while self.queue:
            priority, count, node = heapq.heappop(self.queue)
            if node is not REMOVED:
                del self.find[node]
                return node
        raise KeyError("Pop From Empty Priority Queue")

    def rem(self, node: EightPuzzleNode):
        entry = self.find.pop(node)
        entry[-1] = REMOVED
        # TODO: 3
        # Note that you have to create a data structure here and
        # implement the rest of the abstract methods.


REMOVED = -999


class AStarFrontier(Frontier):
    """A frontier for greedy search."""

    def __init__(self, h_func, goal_state):
        self.goal = goal_state
        self.h = h_func
        self.queue = []
        self.enqueued = {}
        self.counter = itertools.count()

    def is_empty(self):  # return empty value
        return len(self.queue) == 0

    def add(self, node: EightPuzzleNode):
        if node in self.enqueued:
            self.rem(node)
        count = next(self.counter)

        priority = self.calculate(node)
        entry = [priority, count, EightPuzzleNode]
        self.enqueued[EightPuzzleNode] = entry
        heapq.heappush(self.queue, entry)
        pass

    def next(self):
        while self.queue:
            priority, count, node = heapq.heappop(self.queue)
            if node is not REMOVED:
                del self.enqueued[node]
                return node
        raise KeyError("Pop From Empty Priority Queue")

    def rem(self, node: EightPuzzleNode):
        entry = self.enqueued.pop(node)
        entry[-1] = REMOVED

    def calculate(self, node: EightPuzzleNode):
        return node.path_cost + self.h(node.state, self.goal)
        """
        Create a frontier.

        Parameters
        ----------
        h_func : callable h(state)
            a heuristic function to score a state.


        """

        # TODO: 4
        # Note that you have to create a data structure here and
        # implement the rest of the abstract methods.


def _parity(board):
    """Return parity of a square matrix."""
    inversions = 0
    nums = []
    for row in board:
        for value in row:
            nums.append(value)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] != 0 and nums[j] != 0 and nums[i] > nums[j]:
                inversions += 1
    return inversions % 2


def _is_reachable(board1, board2):
    """Return True if two N-Puzzle state are reachable to each other."""
    return _parity(board1) == _parity(board2)


def graph_search(init_state, goal_state, frontier):
    """
    Search for a plan to solve problem.

    Parameters
    ----------
    init_state : EightPuzzleState
        an initial state
    goal_state : EightPuzzleState
        a goal state
    frontier : Frontier
        an implementation of a frontier which dictates the order of exploreation.

    Returns
    ----------
    plan : List[string] or None
        A list of actions to reach the goal, None if the search fails.
        Your plan should NOT include 'INIT'.
    num_nodes: int
        A number of nodes generated in the search.

    """
    if not _is_reachable(init_state.board, goal_state.board):
        return None, 0
    if init_state.is_goal(goal_state.board):
        return [], 0
    num_nodes = 0
    solution = []
    # Perform graph search
    root_node: EightPuzzleNode = EightPuzzleNode(init_state, action='INIT')
    nodeset = set()
    frontier.add(root_node)
    num_nodes += 1

    while not frontier.is_empty():
        currentNode = frontier.next()
        if currentNode.is_goal():
            result = currentNode
            break

        if currentNode.state not in nodeset:
            nodeset.add(currentNode.state)
            num_nodes += 1

        for i in getnode(currentNode ):
            frontier.add(i)

    path = result.trace()
    path.pop(0)

    for i in path:
        solution.append(i.action)
    print(str(len(path)) + " Levels")
    return solution, num_nodes


def getnode(currentNode:EightPuzzleNode):
    Nodes = []
    getmove = Action(currentNode.state,currentNode.state.y, currentNode .state.x)

    for i in getmove:
        movement: EightPuzzleState = currentNode.state.successor(i)
        Nodes.append(EightPuzzleNode(movement, currentNode, i))
    return Nodes

    # TODO: 5


def Action(state: EightPuzzleState, i: int, j: int):
    possibleAction = copy.deepcopy(state.action_space)

    # Coordinate
    # i-1 , j-1 |  i-1 , j  | i-1 , j+1
    # i   , j-1 | [i   , j] | i   , j+1
    # i+1 , j-1 |  i+1 , j  | i+1 , j+1

    row_upper = i - 1
    if row_upper < 0:
        possibleAction.remove('u')

    row_under = i + 1
    if row_under > len(state.board) - 1:
        possibleAction.remove('d')

    col_left = j - 1
    if col_left < 0:
        possibleAction.remove('l')

    col_right = j + 1
    if col_right > len(state.board[0]) - 1:
        possibleAction.remove('r')

    return possibleAction
    pass


def test_by_hand(verbose=True):
    """Run a graph-search."""
    goal_state = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    init_state = EightPuzzleState.initializeState()
    while not _is_reachable(goal_state.board, init_state.board):
        #init_state = EightPuzzleState.initializeState()

        init_state = EightPuzzleState([[7, 8, 3], [0, 4, 1], [2, 5, 6]])
    # frontier = GreedyFrontier(eightPuzzleH2, goal_state)
    frontier = AStarFrontier(eightPuzzleH2, goal_state)
    #frontier = DFSFrontier()  # Change this to your own implementation.

    if verbose:
        print(init_state)
    plan, num_nodes = graph_search(init_state, goal_state, frontier)
    if verbose:
        print(f'A solution is found after generating {num_nodes} nodes.')
    if verbose:
        for action in plan:
            print(f'- {action}')
    return len(plan), num_nodes


def experiment(n=10000):
    """Run experiments and report number of nodes generated."""
    result = defaultdict(list)
    for __ in range(n):
        d, n = test_by_hand(False)
        result[d].append(n)
    max_d = max(result.keys())
    for i in range(max_d + 1):
        n = result[d]
        if len(n) == 0:
            continue
        print(f'{d}, {len(n)}, {sum(n) / len(n)}')


if __name__ == '__main__':
    __, __ = test_by_hand()
    experiment()  # run graph search 10000 times and report result.
