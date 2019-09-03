"""A module for homework 1."""
import random
import copy


class EightPuzzleState:
    """A class for a state of an 8-puzzle game."""

    def __init__(self, board):
        """Create an 8-puzzle state."""
        self.action_space = {'u', 'd', 'l', 'r'}
        self.board = board
        for i, row in enumerate(self.board):
            for j, v in enumerate(row):
                if v == 0:
                    self.y = i
                    self.x = j

    def __repr__(self):
        """Return a string representation of a board."""
        output = []
        for row in self.board:
            row_string = ' | '.join([str(e) for e in row])
            output.append(row_string)
        return ('\n' + '-' * len(row_string) + '\n').join(output)

    def __str__(self):
        """Return a string representation of a board."""
        return self.__repr__()

    @staticmethod
    def initializeState():
        
        Arr = list(range(0,9)) # Create Array value 0 - 8 
        random.shuffle(Arr) # Shuffle by using Random func. 
        count = 0 # Init value to contain to nested list สร่างมาเก็บค่าไปทำ array listed
        nestlist = [] # create empty array 
        for x in range(0,3): # use for loop condition to pack them into nested list (2D-Array) 
            row = []
            for y in range(0,3):
                row.append(Arr[count])  # append shuffle value into row array 
                count += 1
            nestlist.append(row) # append array into array again 
        
        return EightPuzzleState(nestlist)
        pass
        """
        Create an 8-puzzle state with a SHUFFLED tiles.
        
        Return
        ----------
        EightPuzzleState
            A state that contain an 8-puzzle board with a type of List[List[int]]: 
            a nested list containing integers representing numbers on a board
            e.g., [[0, 1, 2], [3, 4, 5], [6, 7, 8]] where 0 is a blank tile.
        """
        # TODO: 1
        

    def successor(self, action):
        if action not in self.action_space:
            raise ValueError(f'`action`: {action} is not valid.')
        # TODO: 2
        # YOU NEED TO COPY A BOARD BEFORE MODIFYING IT
        new_board = copy.deepcopy(self.board)

        AxisX = self.x
        AxisY = self.y
        if action == 'u':
            AxisY = (self.y) - 1
        elif action == 'd':
            AxisY = (self.y) + 1
        elif action == 'l':
            AxisX = (self.x) - 1
        elif action == 'r':
            AxisX = (self.x) + 1
        if AxisX == -1 or AxisY == -1:
            return None
        if AxisX == 3 or AxisY == 3:
            return None
            
        new_board[self.y][self.x]=new_board[AxisY][AxisX]
        new_board[AxisY][AxisX] = 0    
        return EightPuzzleState(new_board)         
        """
        Move a blank tile in the current state, and return a new state.

        Parameters
        ----------
        action:  string 
            Either 'u', 'd', 'l', or 'r'.

        Return
        ----------
        EightPuzzleState or None
            A resulting 8-puzzle state after performing `action`.
            If the action is not possible, this method will return None.

        Raises
        ----------
        ValueError
            if the `action` is not in the action space
        
        """  

    def is_goal(self, goal_board=[[1, 2, 3], [4, 5, 6], [7, 8, 0]]):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                if self.board[i][j] != goal_board[i][j]:
                    return False
        return True
        """
        Return True if the current state is a goal state.
        
        Parameters
        ----------
        goal_board (optional)
            The desired state of 8-puzzle.

        Return
        ----------
        Boolean
            True if the current state is a goal.
        
        """
        # TODO: 3
        
class EightPuzzleNode:
    """A class for a node in a search tree of 8-puzzle state."""
    
    def __init__(self, state, parent=None, action=None, cost=1):
        """Create a node with a state."""
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        if parent is not None:
            self.path_cost = parent.path_cost + self.cost
        else:
            self.path_cost = 0

    def trace(self):
        Nodes = []
        # currentNode = self
        while self.parent is not None:
            Nodes.append(self)
            self = self.parent
        Nodes.reverse()
        # print(currentNode)
        return Nodes
        """
        Return a path from the root to this node.

        Return
        ----------
        List[EightPuzzleNode]
            A list of nodes stating from the root node to the current node.

        """
        # TODO: 4
        pass


def test_by_hand():
    """Run a CLI 8-puzzle game."""
    state = EightPuzzleState.initializeState()
    root_node = EightPuzzleNode(state, action='INIT')
    cur_node = root_node
    print(state)
    action = input('Please enter the next move (q to quit): ')
    while action != 'q':
        new_state = cur_node.state.successor(action)
        cur_node = EightPuzzleNode(new_state, cur_node, action)
        print(new_state)
        if new_state.is_goal():
            print('Congratuations!')
            break
        action = input('Please enter the next move (q to quit): ')

    print('Your actions are: ')
    for node in cur_node.trace():
        print(f'  - {node.action}')
    print(f'The total path cost is {cur_node.path_cost}')


if __name__ == '__main__':
    test_by_hand()