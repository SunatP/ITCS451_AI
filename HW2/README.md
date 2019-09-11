# HW 2 8-Puzzle solve AI (Auto Mode)

## มี 5 TODO ที่ต้องทำ
    1.  def eightPuzzleH1(state, goal_state):
    เป็นฟังก์ชันที่เอาไว้นับค่าหา h1(N) ของ Puzzle จากจุดเริ่มต้นและจุดสิ้นสุดรวมถึงการเลื่อนไปผิดตำแหน่งรวมถึงช่องว่างด้วย
    2.  def eightPuzzleH2(state, goal_state):
    เป็นฟังก์ชันหาค่าระยะทางแบบ Manhattan โดยใช้รูปแบบกระดานที่สมบูรณ์มาหาการกระจัด(ระยะทางที่เร็วที่สุด)
    3.  class GreedyFrontier(Frontier):
    เป็นฟังก์ชัน(อัลกอริทึ่ม)เพื่อแก้ปัญหาสำหรับ 8-Puzzle ให้เหมาะสมกับสถานการณ์นั้นๆ
    4.  class AStarFrontier(Frontier):
    เป็นฟังก์ชัน(อัลกอริทึ่ม)เพื่อแก้ปัญหาสำหรับ 8-Puzzle ใช้หาความน่าจะเป็นได้ดีที่สุด
    5.  def graph_search(init_state, goal_state, frontier):
    เป็นฟังก์ชันค้นหาในรูปแบบโหนดเพื่อหารูปแบบที่เหมาะสมในการแก้ปัญหา 8-Puzzle

### ก่อนจะเขียนเราต้อง import อะไรมาใช้บ้าง
```python
import abc
from collections import defaultdict
from hw1 import EightPuzzleState, EightPuzzleNode
"""
สามอย่างนี้เป็นตัวเริ่มต้นที่มีมาให้ เราจะเพิ่มลงไปอีกคือ
"""
import copy # ไว้สำหรับ copy board เพื่อเอาผลลัพธ์ออกมา
import heapq # ไว้สำหรับ node โดยเฉพาะ
import itertools # ไว้นับค่า
from typing import List, Any
```


### 1. def eightPuzzleH1(state, goal_state):
```python
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
```

เราจะต้องทำการส่งค่าที่ h1(N) หรือค่าที่นับการเคลื่อนที่ของ 8-Puzzle โดยใช้การวิเคราะห์จุดเริ่มต้นกับจุดสุดท้ายและค่าที่ส่งกลับ(Return)จะเป็น Integer

ตัวอย่างในภาษาซี
```C++
    int EightPuzzleH1(int state[n][n], int goal[n][n])
    {
        int misplaced = 0;
        for(i = 0 ; i< n;i++)
            for(j = 0 ; j<n;j++)
                if(state[i][j]!=goal[i][j])
                    misplaced += 1;
        return misplaced;
    }
```
ถ้าเป็น Python โค้ดหน้าตาใน Python จะเป็นอย่างนี้
```python
    def eightPuzzleH1(state, goal_state):
        """
         ในฟังก์ชันนี้เราจะใช้ for loop มาใช้
         เพื่อเปรียบเทียบกระดาน 8-Puzzle ทุกครั้งที่มีการขยับ
        """
        sum = 0 # สร้างตัวแปรมาเก็บค่าใน for loop
        goal_board = goal_state.board # ตรงนี้คืออะไร?
        # goal_board คือตัวแปรที่สร้างมาเช็คตารางหากตารางทั้งสองมีค่าไม่เท่ากันจะทำให้ตัวแปร sum เพิ่มค่าทีละ 1
        # ส่วน goal_state.board นั้น ส่วนแรก goal_state เปรียบเหมือนการใช้ pointer ชี้ไปที่ Class ของ EightPuzzleState ใน hw1 ส่วน board นั้นเป็น value ที่ EightPuzzleState สามารถเรียกออกมาใช้ได้
        for x in range(len(goal_board)):
            for y range(len(goal_board[0])):
                if goal_board[x][y] != goal_board[x][y]:
                    sum += 1
        return sum
```

หรือจะเรียกใช้ฟังก์ชันแบบระบุ class จาก hw1 จะได้แบบนี้

```python
    def eightPuzzleH1(state: EightPuzzleState, goal_state: EightPuzzleState): # ตรง (state,goal_state เราสามารถเพิ่ม : ตามหลังตัวแปรเพื่อชี้ไปหา class ที่ต้องการได้)
        """
         ในฟังก์ชันนี้เราจะใช้ for loop มาใช้
         เพื่อเปรียบเทียบกระดาน 8-Puzzle ทุกครั้งที่มีการขยับ
        """
        sum = 0 # สร้างตัวแปรมาเก็บค่าใน for loop
        goal_board = goal_state.board # ตรงนี้คืออะไร?
        # goal_board คือตัวแปรที่สร้างมาเช็คตารางหากตารางทั้งสองมีค่าไม่เท่ากันจะทำให้ตัวแปร sum เพิ่มค่าทีละ 1
        # ส่วน goal_state.board นั้น ส่วนแรก goal_state เปรียบเหมือนการใช้ pointer ชี้ไปที่ Class ของ EightPuzzleState ใน hw1 ส่วน board นั้นเป็น value ที่ EightPuzzleState สามารถเรียกออกมาใช้ได้
        for x in range(len(goal_board)):
            for y range(len(goal_board[0])):
                if goal_board[x][y] != goal_board[x][y]:
                    sum += 1
        return sum
```

ใน for loop ของ TODO 1 เราสามารถเขียนได้อีกแบบคือ
```python
    sum = 0
    goal_board = goal_state.board
    for x,y in range(len(goal_board),len(goal_board[0])):
        if goal_board[x][y] != goal_board[x][y]:
            sum += 1
    return sum
    
```


### 2. def eightPuzzleH2(state, goal_state):
```python
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
```

เราจะต้องทำการส่งค่าที่จากการวัดระยะแบบ Manhattan จากจุดสุดท้ายของการเคลื่อนที่ทั้งหมดคล้ายกับฟังก์ชัน eightPuzzleH1 

นี่คือการคิดแบบ Brute Force แบบใช้ Nested Loop แบบคร่าวๆ
```c++
for (i = 1; i < n; i++)
  for (j = i + 1; j < n; j++)
    sum += ((xi – xj) + (yi – yj))
```

แต่ต้องใส่ abs หรือ absolute ไว้ด้วยในกรณีที่บางค่ามีการติดลบซึ่งไม่สามารถนำมาใช้ได้

```c++
for (int i = 0; i < n; i++) 
    for (int j = i + 1; j < n; j++) 
        sum += (abs(x[i] - x[j]) +  abs(y[i] - y[j])); 
return sum; 
```

ซึ่งถ้านำมาเขียนในฟังก์ชัน Python จะมีหน้าตาแบบนี้

```python
def eightPuzzleH2(state, goal_state):
    goal_board = goal_state.board
    sum = 0
    for num in range(9):
        for i in range(0, 3, 1):
            for j in range(0, 3, 1):
                if goal_board[i][j] == num:
                    goalPositions = (i, j)


                if state.board[i][j] == num:
                    currPositions = (i, j)


        AxisX = abs(goalPositions[1] - currPositions[1])
        AxisY = abs(goalPositions[0] - currPositions[0])

        sum += AxisY + AxisX

    return sum
```

หรือแบบนี้ก็ได้

```python
def eightPuzzleH2(state, goal_state):
    goal_board = goal_state.board
    sum = 0
    for num in range(0,9):
        for i in range(len(goal_board)):
            for j in range(len(goal_board[0])):
                if goal_board[i][j] == num:
                    goalPositions = (i, j)

                if state.board[i][j] == num:
                    currPositions = (i, j)

        sum += abs(goalPositions[0] - currPositions[0]) + abs(goalPositions[1] - currPositions[1])

    return sum
```

### 3. class GreedyFrontier(Frontier):

```python
    """
    Create a frontier.

    Parameters
    ----------
    h_func : callable h(state, goal_state)
        a heuristic function to score a state.
    goal_state : EightPuzzleState
        a goal state used to compute h()
    """
    self.h = h_func
    self.goal = goal_state
    # TODO: 3
    # Note that you have to create a data structure here and
    # implement the rest of the abstract methods.
```

เราจะต้องสร้าง data structure เพื่อดึงข้อมูลมาคิดในฟังก์ชัน GreedyFrontier

เราจะต้องสร้างอะไรบ้างเพื่อเก็บข้อมูล

    -  ฟังก์ชัน is_empty เพื่อทำให้ค่าที่อยู่ใน queue เป็นศูนย์หรือไม่มี(บ๋อแบ๋)
    -  ฟังก์ชัน add เพื่อทำการเติมโหนดเข้าไปทุกครั้งที่เราหาค่าเจอแต่ถ้ามีอยู่แล้วก็สามารถทำการเอาออกได้ (push)
    -  ฟังก์ชัน next จะเป็นการนำค่าที่น้อยที่สุดเอาออกไปจากโหนด (pop) และลบโหนดที่เข้าคิวอยู่
    -  ฟังก์ชัน remove ที่ใช้คู่กับ add เพื่อเอาค่าที่น้อยที่สุดออกจากโหนด

มาเริ่มที่ **def __init__(self, h_func, goal_state):** กันก่อนเราจะต้องสร้างตัวแปรที่เก็บค่า dict กับ list และ ตัว counter เพิ่อนับค่า

```python 
    def __init__(self, h_func, goal_state):
        self.h = h_func
        self.goal = goal_state
        self.queue = [] # เพิ่ม
        self.find = {} # เพิ่ม
        self.counter = itertools.count() # เพิ่ม
    pass
```

**[]** กับ **{}** ต่างกันอย่างไร [] คือ List เป็น standard array ส่วน {} คือ dict เก็บค่าแบบ associative array

มาดูที่ฟังก์ชันเขียนแบบใช้ **node** แล้วชี้ไปที่คลาส **EightPuzzleNode**
```python
    def is_empty(self):
        return len(self.queue) == 0
        # len คือค่าในรูปแบบ object 
        # การ Return แบบนี้คือ รีเทิร์น object ที่มี array เป็น 0

    def add(self,node: EightPuzzleNode):
        # หรือจะเขียนแบบ def add(self,EightPuzzleNode) ก็ได้
        if node in self.find: # หรือ if EightPuzzleNode in self.find:
            self.remove(node) # หรือ self.remove(EightPuzzleNode)
        count = next(self.counter)

        priority = self.h(node.state, state.goal) # หรือ self.h(EightPuzzleNode.state, state.goal)
        entry = [priority, count, node] # เปลี่ยน node เป็น EightPuzzleNode ก็ได้
        self.find[node] = entry
        heapq.heappush(self.entry)
        pass

    def next(self):
        while self.queue:
            priority, count, EightPuzzleNode = heapq.heappop(self.queue)
            if node is not -9999: # -9999 คือ REMOVED จริงๆจะ Defined แบบไหนก็ได้ขอแค่ตัวเราเข้าใจก็พอ
                del self.find[node]
                return node
            raise KeyError("Pop From Empty Priority Queue") # ใส่ไว้กรณีไม่มีค่าออกมา
    
    def remove(self, node: EightPuzzleNode):
        entry = self.find.pop(node)
        entry[-1] = -9999 
```

แบบไม่ใช้โหนด ใช้ Class EightPuzzleNode เรียกมาเลย
```python
    def is_empty(self):
        return len(self.queue) == 0

    def add(self, EightPuzzleNode):
        if EightPuzzleNode in self.find:
            self.remove(EightPuzzleNode)
        count = next(self.counter)

        priority = self.h(EightPuzzleNode.state, self.goal)
        entry = [priority, count, EightPuzzleNode]
        self.find[EightPuzzleNode] = entry
        heapq.heappush(self.queue, entry)
        pass

    def next(self):
        while self.queue:
            priority, count, EightPuzzleNode = heapq.heappop(self.queue)
            if EightPuzzleNode is not -9999:
                del self.find[EightPuzzleNode]
                return EightPuzzleNode
        raise KeyError("Pop From Empty Priority Queue")

    def remove(self, EightPuzzleNode):
        entry = self.find.pop(EightPuzzleNode)
        entry[-1] = -9999

```

ผลลัพธ์เมื่อเขียนเสร็จหน้าตาจะเป็นแบบนี้
```python
class GreedyFrontier(Frontier):

    def __init__(self, h_func, goal_state):
        self.h = h_func
        self.goal = goal_state
        self.queue = []
        self.find = {}
        self.counter = itertools.count()
    pass

    def is_empty(self):
        return len(self.queue) == 0

    def add(self, EightPuzzleNode):
        if EightPuzzleNode in self.find:
            self.remove(EightPuzzleNode)
        count = next(self.counter)

        priority = self.h(EightPuzzleNode.state, self.goal)
        entry = [priority, count, EightPuzzleNode]
        self.find[EightPuzzleNode] = entry
        heapq.heappush(self.queue, entry)
        pass

    def next(self):
        while self.queue:
            priority, count, EightPuzzleNode = heapq.heappop(self.queue)
            if EightPuzzleNode is not -9999:
                del self.find[EightPuzzleNode]
                return EightPuzzleNode
        raise KeyError("Pop From Empty Priority Queue")

    def remove(self, EightPuzzleNode):
        entry = self.find.pop(EightPuzzleNode)
        entry[-1] = -9999

```


### 4. class AStarFrontier(Frontier):

```python
    """
    Create a frontier.

    Parameters
    ----------
    h_func : callable h(state)
        a heuristic function to score a state.
    goal_state : EightPuzzleState
        a goal state used to compute h()

    """
    # TODO: 4
    # Note that you have to create a data structure here and
    # implement the rest of the abstract methods
```

TODO 4 กับ TODO 3 มีความคล้ายกันดังนั้นสามารถเขียนแบบเดียวกันได้

มาดูที่ฟังก์ชันเขียนแบบใช้ **node** แล้วชี้ไปที่คลาส **EightPuzzleNode**
```python
    def is_empty(self):
        return len(self.queue) == 0
        # len คือค่าในรูปแบบ object 
        # การ Return แบบนี้คือ รีเทิร์น object ที่มี array เป็น 0

    def add(self,node: EightPuzzleNode):
        # หรือจะเขียนแบบ def add(self,EightPuzzleNode) ก็ได้
        if node in self.find: # หรือ if EightPuzzleNode in self.find:
            self.remove(node) # หรือ self.remove(EightPuzzleNode)
        count = next(self.counter)

        priority = self.h(node.state, state.goal) # หรือ self.h(EightPuzzleNode.state, state.goal)
        entry = [priority, count, node] # เปลี่ยน node เป็น EightPuzzleNode ก็ได้
        self.find[node] = entry
        heapq.heappush(self.entry)
        pass

    def next(self):
        while self.queue:
            priority, count, EightPuzzleNode = heapq.heappop(self.queue)
            if node is not -9999: # -9999 คือ REMOVED
                del self.find[node]
                return node
            raise KeyError("Pop From Empty Priority Queue") # ใส่ไว้กรณีไม่มีค่าออกมา
    
    def remove(self, node: EightPuzzleNode):
        entry = self.find.pop(node)
        entry[-1] = -9999 
```

แบบไม่ใช้โหนด ใช้ Class EightPuzzleNode เรียกมาเลย
```python
    def is_empty(self):
        return len(self.queue) == 0

    def add(self, EightPuzzleNode):
        if EightPuzzleNode in self.find:
            self.remove(EightPuzzleNode)
        count = next(self.counter)

        priority = self.h(EightPuzzleNode.state, self.goal)
        entry = [priority, count, EightPuzzleNode]
        self.find[EightPuzzleNode] = entry
        heapq.heappush(self.queue, entry)
        pass

    def next(self):
        while self.queue:
            priority, count, EightPuzzleNode = heapq.heappop(self.queue)
            if EightPuzzleNode is not -9999:
                del self.find[EightPuzzleNode]
                return EightPuzzleNode
        raise KeyError("Pop From Empty Priority Queue")

    def remove(self, EightPuzzleNode):
        entry = self.find.pop(EightPuzzleNode)
        entry[-1] = -9999
```

เนื่องจากคล้ายกับ TODO 3 หน้าตาจะออกมาเป็นแบบนี้

```python
class AStarFrontier(Frontier):

    def __init__(self, h_func, goal_state):
        self.goal = goal_state
        self.h = h_func
        self.queue = []
        self.enqueued = {}
        self.counter = itertools.count()

    def is_empty(self):
        return len(self.queue) == 0

    def add(self, node: EightPuzzleNode):
        if node in self.enqueued:
            self.remove(node)
        count = next(self.counter)

        priority = node.path_cost + self.h(node.state, self.goal)
        entry = [priority, count, node]
        self.enqueued[node] = entry
        heapq.heappush(self.queue, entry)
        pass

    def next(self):
        while self.queue:
            priority, count, node = heapq.heappop(self.queue)
            if node is not -9999:
                del self.enqueued[node]
                return node
        raise KeyError("Pop From Empty Priority Queue")

    def remove(self, node: EightPuzzleNode):
        entry = self.find.pop(node)
        entry[-1] = -9999
```

### ใน TODO ที่ 3 และ 4 สามารถลบฟังก์ชั่น Remove ออกแล้ว โค้ดหน้าตาจะออกมาประมาณนี้

```python
def __init__(self, h_func, goal_state):
        self.goal = goal_state
        self.h = h_func
        self.queue = []
        self.enqueued = {}
        self.counter = itertools.count()

    def is_empty(self):
        return len(self.queue) == 0

    def add(self, node: EightPuzzleNode):
        if node in self.enqueued:
            EightPuzzleNode = self.find.pop(EightPuzzleNode)
            EightPuzzleNode[-1] = -9999
        count = next(self.counter)

        priority = node.path_cost + self.h(node.state, self.goal)
        entry = [priority, count, node]
        self.enqueued[node] = entry
        heapq.heappush(self.queue, entry)
        pass

    def next(self):
        while self.queue:
            priority, count, node = heapq.heappop(self.queue)
            if node is not -9999:
                del self.enqueued[node]
                return node
        raise KeyError("Pop From Empty Priority Queue")
```
**def remove(self):** นั้นสามารถแทนด้วย self.find.pop(EightPuzzleNode) ซึ่งมาจาก heapq ไลบรารี่ซึ่งทำให้โค้ดนั้นสั้นลงได้

### 5. def graph_search(init_state, goal_state, frontier):

```python
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
    root_node = EightPuzzleNode(init_state, action='INIT')
    num_nodes += 1

    # TODO: 5

    return solution, num_nodes
```

เราจะต้องสร้าง condition หรือเงื่อนไขเพื่อหา Frontier หรือผลลัพธ์ออกมา <br>
```python
def graph_search(init_state, goal_state, frontier):
    if not _is_reachable(init_state.board, goal_state.board):
        return None, 0
    if init_state.is_goal(goal_state.board):
        return [], 0
    num_nodes = 0
    solution = []
    # Perform graph search
    root_node: EightPuzzleNode = EightPuzzleNode(init_state, action='INIT')
    frontier.add(root_node) # เพิ่ม
    num_nodes += 1
    nodeset = set() # เพิ่ม เซ็ตเป็นกลุ่มข้อมูลคล้ายๆกับ list

    while not frontier.is_empty(): # เช็คว่า frontier นั้นมีค่าหรือไม่ เช็คจาก AStarFrontier()
        CurrentNode = frontier.next() # ตัวแปรนี้จะนำไปหา frontier ตัวต่อไป
        if CurrentNode.state.is_goal(): # เช็คว่า CurrentNode นั้นถูกกับ goal_board หริอไม่
            result = CurrentNode  
            break

        if CurrentNode.state not in nodeset: # เช็คว่า CurrentNode ไม่ได้อยู่ใน set()
            nodeset.add(currentNode.state) # ถ้าไม่อยู่ให้เอา CurrentNode ใส่เข้าไปใน nodeset
            num_nodes += 1

            for i in getnode(currentNode): # ใช้ for ลูปเพื่อหาค่าในฟังก์ชัน getnode เพื่อเอา movement ออกมา
                frontier.add(i)
    path = result.trace() # เอาผลลัพธ์ออกมา generate 
    path.pop(0) # เพื่อไม่ให้ - INIT ออกมา

    for i in path: # ใช้ for loop โดยใช้ path เป็น condition
        solution.append(i.action) # ถ้ามีค่า ให้เอา frontier ใส่ลงไปใน solution ที่เป็น list
    return solution, num_nodes

def getnode(currentNode: EightPuzzleNode): # ฟังก์ชันนี้ไว้ใช้ระบุ path ไว้เดิน
    Nodes = []
    def check(state: EightPuzzleState,i,j):
        board = copy.deepcopy(state.action_space)
        if i - 1 < 0 :
            board.remove('u')

        if i + 1 > len(state.board) - 1:
            board.remove('d')

        if j - 1 < 0:
            board.remove('l')

        if j + 1 > len(state.board[0]) - 1:
            board.remove('r')

        return board
        pass

      moveAction = check(currentNode.state, currentNode.state.y, currentNode.state.x)

    for i in moveAction: # ใช้ for loop โดยใช้ moveAction เป็น Condition
        movement: EightPuzzleState = currentNode.state.successor(i) # movement เป็นการ ชี้ไปที่ EightPuzzleNode-> successor เพื่อดึง movement ออกมา
        Nodes.append(EightPuzzleNode(movement, currentNode, i)) # เอา movement ที่ได้ใส่ลง List
    return Nodes

```
หรือแบบนี้
```python
    while frontier.is_empty() == False:
        current = frontier.next()
        if current.state.is_goal() == True:
            result = current
            break
        if current.state not in setnode:
            setnode.add(current.state)
            num_nodes += 1
            Nodes=[]

            board = copy.deepcopy(EightPuzzleState.action_space)
            if current.state.y - 1 < 0:
                board.remove('u')
            if current.state.y + 1 > len(EightPuzzleState.board) - 1:
                board.remove('d')
            if current.state.x - 1 < 0:
                board.remove('l')
            if current.state.x + 1 > len(EightPuzzleState.board[0]) - 1:
                board.remove('r')
            for i in board:
                EightPuzzleState2 = current.state.successor(i)
                Nodes.append(EightPuzzleNode(EightPuzzleState2, current, i))
            for i in Nodes:
                frontier.add(i)
    path = result.trace()
    path.pop(0)
    print ( path)
    for i in path:
        solution.append(i.action)
    return solution, num_nodes
```



### วิธีรันโค้ด
หน้าตาตอนแรก
```python
def test_by_hand(verbose=True):
    """Run a graph-search."""
    goal_state = EightPuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    init_state = EightPuzzleState.initializeState()
    while not _is_reachable(goal_state.board, init_state.board):
        init_state = EightPuzzleState.initializeState()
    # frontier = GreedyFrontier(eightPuzzleH1, goal_state)
    frontier = AStarFrontier(eightPuzzleH2, goal_state)   
    # frontier = DFSFrontier()  # Change this to your own implementation.
    if verbose:
        print(init_state)
    plan, num_nodes = graph_search(init_state, goal_state, frontier)
    if verbose:
        print(f'A solution is found after generating {num_nodes} nodes.')
    if verbose:
        for action in plan:
            print(f'- {action}')
    return len(plan), num_nodes

```
เวลารันต้องเอา **#** ออกก่อน

```python
    frontier = GreedyFrontier(eightPuzzleH1, goal_state)
    # frontier = AStarFrontier(eightPuzzleH2, goal_state)
    # frontier = DFSFrontier()  # Change this to your own implementation.
    
```
หรือ 

```python
    # frontier = GreedyFrontier(eightPuzzleH1, goal_state)
    frontier = AStarFrontier(eightPuzzleH2, goal_state)
    # frontier = DFSFrontier()  # Change this to your own implementation.
    
```

และก็ตรงแก้ตรงนี้ด้วย 

```python
if __name__ == '__main__':
    __, __ = test_by_hand()
    # experiment()  # run graph search 10000 times and report result.

    """
    ตรง experiment ถ้าเราจะรันให้เอา # ออกก่อนแล้วใส่ # ตรง __, __ = test_by_hand()
    """
```