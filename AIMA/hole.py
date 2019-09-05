"""A module for homework 1."""
# noqa: D413

import abc
import copy
import heapq
import itertools
from collections import defaultdict
from typing import List, Any

from hw1 import EightPuzzleState, EightPuzzleNode


def eightPuzzleH1(state: EightPuzzleState):
    """
    Return the number of misplaced tiles including blank.

    Parameters
    ----------
    state: EightPuzzleState
        an 8-puzzle state containing a board (List[List[int]])

    Returns
    ----------
    int

    """
    # TODO 1:
    goal_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    misplaceCount = 0

    for i in range(len(goal_board)):
        for j in range(len(goal_board[0])):
            if goal_board[i][j] != state.board[i][j]:
                misplaceCount += 1

    return misplaceCount


def eightPuzzleH2(state: EightPuzzleState):
    """
    Return the total Manhattan distance from goal position of all tiles.

    Parameters
    ----------
    state: EightPuzzleState
        an 8-puzzle state containing a board (List[List[int]])

    Returns
    ----------
    int

    """
    # TODO 1:
    goal_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    manhattanSum = 0
    for num in range(9):
        foundElemInCurrState = False
        foundElemInGoalState = False

        for i in range(len(goal_board)):
            for j in range(len(goal_board[0])):
                # print(str(goal_board[i][j]) + " " + str(state.board[i][j]))
                if (not foundElemInGoalState) and goal_board[i][j] == num:
                    goalPositions = (i, j)
                    foundElemInGoalState = True

                # print()
                if (not foundElemInCurrState) and state.board[i][j] == num:
                    currPositions = (i, j)
                    foundElemInCurrState = True
            if foundElemInCurrState and foundElemInGoalState:
                break

        manhattanX = abs(goalPositions[1] - currPositions[1])
        manhattanY = abs(goalPositions[0] - currPositions[0])

        manhattanSum += manhattanY + manhattanX

    return manhattanSum


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

    def __init__(self, h_func):
        """
        Create a frontier.

        Parameters
        ----------
        h_func : callable h(state)
            a heuristic function to score a state.


        """
        self.h = h_func
        # TODO: 3
        self.queue = []
        self.entryFinder = {}
        self.counter = itertools.count()

        # Note that you have to create a data structure here and
        # implement the rest of the abstract methods.

    pass

    def is_empty(self):
        return len(self.queue) == 0

    def add(self, node: EightPuzzleNode):
        if node in self.entryFinder:
            self.remove(node)
        count = next(self.counter)

        priority = self.h(node.state)
        entry = [priority, count, node]
        self.entryFinder[node] = entry
        heapq.heappush(self.queue, entry)
        pass

    def next(self):
        while self.queue:
            priority, count, node = heapq.heappop(self.queue)
            if node is not REMOVED:
                del self.entryFinder[node]
                return node
        raise KeyError('pop from an empty priority queue')

    def remove(self, node: EightPuzzleNode):
        entry = self.entryFinder.pop(node)
        entry[-1] = REMOVED


REMOVED = -999


class AStarFrontier(Frontier):
    """A frontier for greedy search."""

    def __init__(self, h_func):
        """
        Create a frontier.

        Parameters
        ----------
        h_func : callable h(state)
            a heuristic function to score a state.


        """
        self.h = h_func

        # TODO: 4
        self.queue = []
        self.entryFinder = {}
        self.counter = itertools.count()

        # Note that you have to create a data structure here and
        # implement the rest of the abstract methods.

    def is_empty(self):
        return len(self.queue) == 0

    def add(self, node: EightPuzzleNode):
        if node in self.entryFinder:
            self.remove(node)
        count = next(self.counter)

        priority = self.calculatePathCostWithHeuristic(node)
        entry = [priority, count, node]
        self.entryFinder[node] = entry
        heapq.heappush(self.queue, entry)
        pass

    def next(self):
        while self.queue:
            priority, count, node = heapq.heappop(self.queue)
            if node is not REMOVED:
                del self.entryFinder[node]
                return node
        raise KeyError('pop from an empty priority queue')

    def calculatePathCostWithHeuristic(self, node: EightPuzzleNode):
        return node.path_cost + self.h(node.state)

    def remove(self, node: EightPuzzleNode):
        entry = self.entryFinder.pop(node)
        entry[-1] = REMOVED


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


def graph_search(init_state: EightPuzzleState, goal_state: EightPuzzleState, frontier: Frontier):
    """
    Search for a plan to solve problem.

    Parameters
    ----------
    init_state : EightPuzzleState
        an initial state
    goal_state : EightPuzzleState
        a goal state
    frontier : Frontier
        an implementation of a frontier which dictates the order of exploration.
    
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

    exploredNodeSet = set()

    frontier.add(root_node)
    num_nodes += 1

    # TODO: 5
    while not frontier.is_empty():
        currentNode = frontier.next()
        # print()
        # print(currentNode.state)
        # frontier.remove(currentNode)
        if currentNode.state.is_goal():
            solutionNode = currentNode
            # print("Current node is Goal")
            break

        if currentNode not in exploredNodeSet:
            exploredNodeSet.add(currentNode)
            num_nodes += 1

            for child in getLeafNodes(currentNode):
                # print("Added\n" + str(child.state))
                frontier.add(child)
        # print(num_nodes)
        # print()

    # print(solutionNode.state)
    tracePath = solutionNode.trace()
    tracePath.reverse()

    # for i in tracePath:
    #     print(i.state)
    #     print()

    for elem in tracePath:
        solution.append(elem.action)
    print(str(len(tracePath)) + " Levels")
    return solution, num_nodes


def getLeafNodes(currentNode: EightPuzzleNode):
    """

    :param currentNode: EightPuzzleNode
    :return:
    """

    leafNodes = []
    possibleMoves = currentNode.state.getPossibleActions(currentNode.state.y, currentNode.state.x)

    for i in possibleMoves:
        currentBoard = copy.deepcopy(currentNode.state.board)
        currentNode.state.move(currentBoard, i)
        leafNodes.append(EightPuzzleNode(EightPuzzleState(currentBoard), currentNode, i))
    return leafNodes


def test_by_hand(verbose=True):
    """Run a graph-search."""
    goal_state = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    init_state = EightPuzzleState.initializeState()
    while not _is_reachable(goal_state.board, init_state.board):
        init_state = EightPuzzleState.initializeState()

    # Change this to your own implementation.
    # frontier = GreedyFrontier(eightPuzzleH2)
    frontier = AStarFrontier(eightPuzzleH2)
    # frontier = DFSFrontier()

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
        d, n = test_by_hand(True)
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
