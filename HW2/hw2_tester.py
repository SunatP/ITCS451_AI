"""Tests for homework 2."""

import unittest

from hw1 import EightPuzzleState, EightPuzzleNode
from hw2 import (
    eightPuzzleH1, eightPuzzleH2, 
    GreedyFrontier, AStarFrontier, 
    graph_search)


class TestGraphSearch(unittest.TestCase):
    """Tests for homework 2."""

    def test_h1(self):
        """Test for TODO 1."""
        a = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 0, 8]])
        b = EightPuzzleState([[2, 1, 3], [6, 5, 7], [4, 8, 0]])
        self.assertEqual(
            eightPuzzleH1(a, b), 7,
            ('There are 7 misplaces between '
            '[[1, 2, 3], [4, 5, 6], [7, 8, 0]] '
            'and [[2, 1, 3], [6, 5, 7], [4, 8, 0]].'))

    def test_h2(self):
        """Test for TODO 2."""
        a = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 0, 8]])
        b = EightPuzzleState([[2, 1, 3], [6, 5, 7], [4, 8, 0]])
        self.assertEqual(
            eightPuzzleH2(a, b), 10,
            ('Total distance between all times of '
            '[[1, 2, 3], [4, 5, 6], [7, 8, 0]] and '
            '[[2, 1, 3], [6, 5, 7], [4, 8, 0]] are 10.'))

    def test_greedy_frontier(self):
        """Test for TODO 3."""
        goal = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        a = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 0, 8]])
        b = EightPuzzleState([[2, 1, 3], [6, 5, 7], [4, 8, 0]])
        c = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

        def h(s1, _s2):
            if s1 == a:
                return 1
            elif s1 == b:
                return 2
            elif s1 == c:
                return 0
            else:
                return 4

        frontier = GreedyFrontier(h, goal)
        self.assertTrue(frontier.is_empty(), 'A new frontier is empty.')
        node_a = EightPuzzleNode(a)
        node_b = EightPuzzleNode(b)
        node_c = EightPuzzleNode(c)
        frontier.add(node_a)
        frontier.add(node_b)
        frontier.add(node_c)
        self.assertFalse(
            frontier.is_empty(),
            'After added nodes, a frontier is not empty.')
        nodes = [frontier.next() for __ in range(3)]
        self.assertEqual(
            nodes, [node_c, node_a, node_b],
            'next() returns nodes in order of their heuristic values (asc).')
        frontier = GreedyFrontier(h, goal)
        a = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        b = EightPuzzleState([[2, 1, 3], [6, 5, 7], [4, 8, 0]])
        c = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        node_a = EightPuzzleNode(a)
        node_b = EightPuzzleNode(b)
        node_c = EightPuzzleNode(c)
        frontier.add(node_a)
        frontier.add(node_b)
        frontier.add(node_c)
        node_1 = frontier.next()
        node_2 = frontier.next()
        self.assertEqual(
            node_1.state, node_a.state, 'Lowest h(n) is returned first.')
        self.assertEqual(
            node_2, node_b, 'A frontier only keeps 1 node with the same state.')

    
    def test_astar_frontier(self):
        """Test for TODO 3."""
        goal = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        a = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 0, 8]])
        b = EightPuzzleState([[2, 1, 3], [6, 5, 7], [4, 8, 0]])
        c = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

        def h(s1, _s2):
            if s1 == a:
                return 1
            elif s1 == b:
                return 2
            elif s1 == c:
                return 0
            else:
                return 4

        frontier = AStarFrontier(h, goal)
        self.assertTrue(frontier.is_empty(), 'A new frontier is empty.')
        node_a = EightPuzzleNode(a)
        node_a.path_cost = 1
        node_b = EightPuzzleNode(b)
        node_b.path_cost = 1
        node_c = EightPuzzleNode(c)
        node_c.path_cost = 5
        frontier.add(node_a)
        frontier.add(node_b)
        frontier.add(node_c)
        self.assertFalse(
            frontier.is_empty(),
            'After added nodes, a frontier is not empty.')
        nodes = [frontier.next() for __ in range(3)]
        self.assertEqual(
            nodes, [node_a, node_b, node_c],
            'next() returns nodes in order of their heuristic values (asc).')
        frontier = AStarFrontier(h, goal)
        a = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        b = EightPuzzleState([[2, 1, 3], [6, 5, 7], [4, 8, 0]])
        c = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        node_a = EightPuzzleNode(a)
        node_a.path_cost = 10
        node_b = EightPuzzleNode(b)
        node_c = EightPuzzleNode(c)
        frontier.add(node_a)
        frontier.add(node_b)
        frontier.add(node_c)
        node_1 = frontier.next()
        node_2 = frontier.next()
        self.assertEqual(
            node_1, node_c, 'Lowest f(n) is returned first.')
        self.assertEqual(
            node_2, node_b, 'A frontier only keeps 1 node with the same state.')

    
    def test_graph_search(self):
        """Test for TODO 4."""
        goal_state = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        init_state = EightPuzzleState([[0, 5, 2,],[1, 4, 8], [7, 6, 3]])
        optim_len = 10
        frontier = AStarFrontier(eightPuzzleH2, goal_state)
        plan, num_nodes = graph_search(init_state, goal_state, frontier)
        self.assertEqual(
            len(plan), optim_len, 
            ('Starting at [[0, 5, 2,],[1, 4, 8], [7, 6, 3]], '
            'the optimal solution only contain 10 actions'))
        self.assertTrue(
            20 <= num_nodes <= 40, 'AStar generated around 29 nodes.')
        cur_state = init_state
        for action in plan:
            cur_state = cur_state.successor(action)
        self.assertEqual(
            cur_state, goal_state, 
            'AStar solution correctly moves the init state to the goal.')

        frontier = GreedyFrontier(eightPuzzleH2, goal_state)
        plan, num_nodes = graph_search(init_state, goal_state, frontier)
        cur_state = init_state
        for action in plan:
            cur_state = cur_state.successor(action)
        self.assertEqual(
            cur_state, goal_state, 
            'Greedy solution correctly moves the init state to the goal.')

if __name__ == '__main__':
    unittest.main()