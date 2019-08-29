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
        
        Arr = list(range(0,9)) # Create Array value 0 - 8 สร้างอาเรย์ที่มีค่า 9 ค่าตั้งแต่ 0 - 8
        random.shuffle(Arr) # Shuffle by using Random func. ใช้ฟังก์ชั่นสุ่มค่าที่มีชื่อว่า Shuffle สุ่มค่าจากตัวแปร Arr
        count = 0 # Init value to contain to nested list สร่างมาเก็บค่าไปทำ array listed
        nestlist = [] # create empty array สร้างอาเรย์เปล่า
        for x in range(0,3): # use for loop condition to pack them into nested list (2D-Array) ใช้ for loop ทำอาเรย์ 2 มิติ
            row = []
            for y in range(0,3):
                row.append(Arr[count])  # append shuffle value into row array เอาค่าจาก Arr ใส่ในอาเรย์ row
                count += 1
            nestlist.append(row) # append array into array again เอาค่าจาก row ใส่ใน nestlisted อีกที ประมาณแบบ อาเรย์ซ้อนกัน [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        
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

        i = self.y
        j = self.x
        # getmovement = self.possibleact(i,j)

        # if len(getmovement) == 0 or action not in getmovement:
        #     return None

        self.move(new_board,action,(i,j)) # move the position of blank tile   

        return EightPuzzleState(new_board)
        pass 

    def move(self,copyboard,direction,blankPosition): # move value by using string
        i = blankPosition[0]
        j = blankPosition[1]

        axisX = i
        axisY = j
        if direction == 'u':
            axisX -= 1
        elif direction == 'd':
            axisX += 1
        elif direction == 'r':
            axisY += 1
        elif direction == 'l':
            axisY -= 1 
            
        tmp = copyboard[i][j]
        copyboard[i][j] = copyboard[axisX][axisY]
        copyboard[axisX][axisY] = tmp
        
        pass

    # def possibleact(self,i,j): 

    #     getmovement = copy.deepcopy(self.action_space)

    #     top_row = i - 1
    #     if top_row < 0 :
    #         getmovement.remove('u')

    #     bottom_row = i + 1
    #     if bottom_row > len(self.board) - 1:
    #         getmovement.remove('d')

    #     left_col = j - 1 
    #     if left_col < 0 :
    #         getmovement.remove('l')
        
    #     right_col = j + 1
    #     if right_col > len(self.board[0]) - 1 :
    #         getmovement.remove('r')

        
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
        
        # return EightPuzzleState(new_board)  
        
        pass

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
        currentNode = self
        while currentNode.parent is not None:
            Nodes.append(currentNode)
            currentNode = currentNode.parent
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