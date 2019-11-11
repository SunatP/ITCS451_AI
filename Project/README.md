# Project 1 Othello V3.0 (AI Player)

Othello with AI by using minimax with Alpha-beta pruning Algorithm

## Due Date 24 November 2019, 11.55 PM (23.55 GMT+07:00)

## มี 2 TODO ที่ต้องทำ (We have 2 TODO to get work)
    1.  TODO แรกจะอยู่ในไฟล์ reversi_agent.py โดยที่เราจะต้องสร้าง abstract class ขึ้นมาแล้วเขียน code search โดยใช้อัลกอริทึ่ม minimax ที่มี Alpha-beta pruning เพื่อเพิ่มประสิทธิภาพ
    2.  TODO สองจะต้องมาแก้ Agent ใน reversi.py เพื่อเอา agent ที่เราเขียนมาลองปรับใช้

### ก่อนจะเขียนเราต้องติดตั้ง อะไรบ้าง (What do we need for this project?)
    1. Numpy
    2. Gym 
    3. tqdm ตัวนี้เป็น progess bar
    4. boardgame2 bg2

### import อะไรมาใช้บ้างใน Reversi_agent.py (What we need to import in our code?)
```python
import sys
import abc
import asyncio
import random
import time
import traceback
from multiprocessing import Process, Value

import gym
import numpy as np
```

### Saving Of Alpha-Beta

The savings of alpha beta can be considerable. If a standard minimax search tree has x nodes, an alpha beta tree in a well-written program can have a node count close to the square-root of x. How many nodes you can actually cut, however, depends on how well ordered your game tree is. If you always search the best possible move first, you eliminate the most of the nodes. Of course, we don't always know what the best move is, or we wouldn't have to search in the first place. Conversely, if we always searched worse moves before the better moves, we wouldn't be able to cut any part of the tree at all! For this reason, good move ordering is very important, and is the focus of a lot of the effort of writing a good chess program. As pointed out by Levin in 1961, assuming constantly b moves for each node visited and search depth n, the maximal number of leaves in alpha-beta is equivalent to minimax, b ^ n. Considering always the best move first, it is b ^ ceil(n/2) plus b ^ floor(n/2) minus one. The minimal number of leaves is shown in following table which also demonstrates the odd-even effect: 

|depth n| b^n  |b^⌈n/2⌉ + b^⌊n/2⌋ - 1|
|:---:|---:|---:|
|0| 1|1|
| 1  | 1  |40|
| 2  | 40  |79|
| 3  | 1,600  |1,639|
| 4  | 64,000 |3,199|
| 5  | 2,560,000  |65,569|
| 6  | 102,400,000  |127,999|
| 7  | 163,840,000,000  |2,623,999|
| 8  | 6,553,600,000,000  |5,119,999|

### Pseudo Minimax with Alpha-Beta Prunning for Othello

อัลกอริทึ่ม (Algorithm of) ของ Minimax with Alpha-Beta Prunning 
![python](https://www.researchgate.net/profile/Dor_Atzmon/publication/329715244/figure/fig1/AS:704844495077383@1545059431887/The-Alpha-Beta-pseudo-code-from-Russell-and-Norvigs-AI-textbook-Russell-and-Norvig.jpg)


```python
"""
    Alpha-Beta Pruning Search Algorithm limit with 10
    -----------------------------------------------
    function ABS(state) return action
    v <- Max_value(state,+inf,-inf) # v = Max_Value
    -----------------------------------------------
    function Max_value(state,alpha,beta) return a utility value
    if Terminal-test(state) then return utility(state)
    v <- (-inf)  # we can define -inf as float('-inf') or -float('inf)
    for each a in action(state) do
    v <- max(v,Min_Value(Result(s,a),alpha,beta))
    if v >= beta then return v
    alpha <- max(alpha,v)
    return v
    -----------------------------------------------
    function Min_value(state,alpha,beta) return a utility value
    if Terminal-test(state) then return utility(state)
    v <- (inf)
    for each a in action(state) do
    v <- min(v,Max_Value(Result(s,a),alpha,beta))
    if v <= alpha then return v
    beta <- max(beta,v)
    return v
    -----------------------------------------------
    function alphabeta(node, depth, α, β, maximizingPlayer) is
    if depth = 0 or node is a terminal node then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
            α := max(α, value)
            if α ≥ β then
                break (* β cut-off *)
        return value
    else
        value := +∞
        for each child of node do
            value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
            β := min(β, value)
            if α ≥ β then
                break (* α cut-off *)
        return value
    (* Initial call *)
    alphabeta(origin, depth, −∞, +∞, TRUE)
    """
```

## 1. reversi_agent.py สร้าง Agent ของเราขึ้นมาเอง (Create our Agent)


เดิมทีอาจารย์จะให้ Agent มา 1 ตัวนั่นก็คือ RandomAgent ซึ่งเป็นตัวสุ่มค่าเล่นกับ AI ของเราเอง เราจะต้องสร้าง class ที่มี Agent ของเราเพื่อมาสู้กับ AI ของอาจารย์นั่นเอง<br>
First Teacher give an Agent in our Project that is RandomAgent AI. This AI will Random value and mark this value in the board, So we need to create our class function to versus Teacher AI Agent!!.

```python
class RandomAgent(ReversiAgent):
    """An agent that move randomly."""

    def search(
            self, color, board, valid_actions,
            output_move_row, output_move_column):
        """Set the intended move to the value of output_moves."""
        try:
            # while True:
            #     pass
            time.sleep(3)
            randidx = random.randint(0, len(valid_actions) - 1)
            random_action = valid_actions[randidx]
            output_move_row.value = random_action[0]
            output_move_column.value = random_action[1]
        except Exception as e:
            print(type(e).__name__, ':', e)
            print('search() Traceback (most recent call last): ')
            traceback.print_tb(e.__traceback__)

```
This is Teacher Agent<br>นี่คือ Agent ของอาจารย์ 

## เริ่มสร้าง Agent ของเรากัน (Let's Create the Agent)

ให้เราสร้าง class ตามด้วยชื่อของเราและมี ReversiAgent ด้วย<br>ตัวอย่าง<br> First we should to create our class with division name or something in class funciton of python, example of Teacher Class
```python
class NorAgent(ReversiAgent):
    ข้างในเป็นโค้ด # Code will be here
```

จากนั้นให้สร้างฟังก์ชั่น ***search*** ใส่ไว้ใน class ที่เราพึ่งสร้างเมื่อกี้นี้ตามตัวอย่าง Agent ของอาจารย์<br>after that we should to create **search** function in our class that we are already create as example teacher's Agent (Implement function) 

```python
class NorAgent(ReversiAgent):
    def search(self, color, board, valid_actions,
            output_move_row, output_move_column):
```

ซึ่ง search ตัวนี้ อ้างอิงมาจาก abstract method จาก class ReversiAgent ของอาจารย์อันนี้<br>This **Search** function reference from abstract method that teacher create ReversiAgent

```python
@abc.abstractmethod
    def search(
            self, color, board, valid_actions,
            output_move_row, output_move_column):
        """
        Set the intended move to self._move.
        The intended move is a np.array([r, c]) where r is the row index
        and c is the column index on the board. [r, c] must be one of the
        valid_actions, otherwise the game will skip your turn.
        Parameters
        -------------------
        board : np.array
            An 8x8 array that contains
        valid_actions : np.array
            An array of shape (n, 2) where n is the number of valid move.
        Returns
        -------------------
        None
            This method should set value for
            `output_move_row.value` and `output_move_column.value`
            as a way to return.
        """
        raise NotImplementedError('You will have to implement this.')

```
เมื่อเราสร้างฟังก์ชัน search เสร็จแล้วให้เราข้ามไปก่อน ให้เราไปสร้างฟังก์ชั่น Alpha-Beta Pruning ขึ้นมาก่อนแล้วค่อยกลับไปทำฟังก์ชั่น search ทีหลัง<br> When we already create Function **search** we will skip this function, then we create Alpha-Beta Pruning after that, we will go back to do this search function again.
```python
"""
function Max_value(state,alpha,beta) return a utility value
    if Terminal-test(state) then return utility(state)
    v <- (-inf)  # we can define -inf as float('-inf') or -float('inf)
    for each a in action(state) do
    v <- max(v,Min_Value(Result(s,a),alpha,beta))
    if v >= beta then return v
    alpha <- max(alpha,v)
    return v
"""
def Max_value(self,board:np.array,validactions:np.array,depth:int,level:int,alpha:float,beta:float,gain:bool):
    if depth == 0:
        countA: int = 0
        countB: int = 0
        evalBoard = np.array(list(zip(*board.nonzero()))) 
        # nonzero จะทำให้ค่าในอาเรย์ที่เราจะสร้างนั้นจะไม่มีค่าออกมาเป็น 0
        # zip คือคำสั่งในการจับคู่ของ value ทั้งสองตัว
        # a = ["a", "b", "c"]
        # b = [1, 2, 3]
        # c = zip(a,b)
        # print(list(c))
        # ผลลัพธ์ที่ได้คือ  [('a', 1), ('b', 2), ('c', 3)]
        for row in evalBoard:
            if board[row[0]][row[1]] == self._color:
                countA += 1
            else:
                countB += 1
        return countA - countB  
    
    Beststate: np.array = None # เราจะสร้างเพื่อใช้อาเรย์ในการเดินตาราง
    MaxAlpha: int = alpha
    Maxevaluation = float('-inf') # หรือจะเขียน -float('inf), -sys.maxsize - 1 ก็ได้  
    for Actions in validactions : # validaction เป็น np.array
        newboard, newaction = self.createState(board,Actions,player) # newboard กับ newaction จะเป็น array แล้วนะ
        # createState เราจะต้องสร้างทีหลัง 
        newmove = self.Min_value(newboard, newaction,depth-1,level+1,MaxAlpha,beta,not gain) # Min_value เราจะต้องสร้างเพิ่ม
        if Maxevaluation < newmove:
            Maxevaluation = newmove

            if level == 0:
                Beststate = Actions
        MaxAlpha = max(MaxAlpha,Maxevaluation)
        if beta <= MaxAlpha: # ใช้การ pruning Node ถ้าเกิดค่า Alpha มากกว่าหรือเท่ากับ beta 
            break
    if level != 0:
        return Maxevaluation
    else:
        Maxevaluation,Beststate

"""
function Min_value(state,alpha,beta) return a utility value
    if Terminal-test(state) then return utility(state)
    v <- (inf)
    for each a in action(state) do
    v <- min(v,Max_Value(Result(s,a),alpha,beta))
    if v <= alpha then return v
    beta <- max(beta,v)
    return v
"""

def Min_value(self,board:np.array,validactions:np.array,depth:int,level:int,alpha:float,beta:float,gain:bool):  
    if depth == 0:
        countA: int = 0
        countB: int = 0
        evalBoard = np.array(list(zip(*board.nonzero())))

        for row in evalBoard:
            if board[row[0]][row[1]] == self._color:
                countA += 1
            else:
                countB += 1
        return countA - countB 
    MinBeta: int = beta
    Minevaluation = float('inf') # เเขียนอีกแบบได้คือ sys.maxsize
    player: int = self.getOpponent(self._color)
    Beststate: np.array = None 
    for Actions in validactions:
        newboard, newaction = self.createState(board,Actions,player)
        newmove = self.Max_value(newstate,newaction,depth-1,level + 1, alpha,MinBeta,not gain)
        if Minevaluation > newmove:
            Minevaluation = newmove

            if level == 0:
                Beststate = Actions

        MinBeta = min(MinBeta,newmove)
        if MinBeta <= alpha:
            break
    if level != 0:
        return Minevaluation
    else:
        return Minevaluation,Beststate

"""
ข้างล่างนี้จะเป็นฟังก์ชั่นเสริม
"""
@staticmethod
def getOpponent(player: int):
    if player == 1:
        return -1
    else:
        return 1   

def createState(self, board: np.array, action: np.array, player: int) -> (np.array, np.array):
    newState: np.array = transition(board, player, action)

    validMoves: np.array = _ENV.get_valid((newState, self.getOpponent(player)))
    validMoves: np.array = np.array(list(zip(*validMoves.nonzero())))

    return newState, validMoves 
```

เมื่อเราสร้างฟังก์ชั่น MiniMax with Alpha Beta Prunning เสร็จแล้วให้กลับเพิ่มโค้ดใน search ต่อ<br>After we create Minimax Function we will back to implement search function again.

```python
class NorAgent(ReversiAgent):
    def search(self, color, board, valid_actions,
            output_move_row, output_move_column):
        # เราจะใช้ try/execept เข้ามาช่วยเพื่อหา error ที่เกิดขึ้น
        try:
            evaluation, best_state = self.Max_value(board,valid_actions,4,0,-float('inf'),float('inf'),True)

            output_move_row.value = best_state[0]
            output_move_column.value = best_state[1]
        except Exception as e:
            print(type(e).__name__, ':', e)
            print('search() Traceback (most recent call last): ')
            traceback.print_tb(e.__traceback__)
        
```
จากนั้นให้ไปที่ **reversi.py** เพื่อเอา Agent เราไปใส่ ให้เรามองหา if __name__ == __**main**__: 
หน้าตาตอนแรกจะเป็นอย่างงี้ให้เรา class ที่เราสร้างนั้นใส่ลงไปแทน<br>Back to **reversi.py** and add the agent that we created it, before we add it looking for main function and replace RandomAgent to Our Agent that we created it.

จาก
```python
if __name__ == "__main__":
    # black = agents.SunatAgent(bg2.BLACK)
    black = agents.RandomAgent(bg2.BLACK)
    white = agents.RandomAgent(bg2.WHITE)
    asyncio.run(main(black, white, 10))
```
เป็น
```python
if __name__ == "__main__":
    # black = agents.SunatAgent(bg2.BLACK)
    black = agents.NorAgent(bg2.BLACK)
    white = agents.RandomAgent(bg2.WHITE)
    asyncio.run(main(black, white, 10))
```

### Result of Othello AI 
Result แบบคร่าวๆ
```bash
Time spent total : ~100.6128 - 180.4286 Seconds # alpha & beta is -2080,2080 vs Pooh Agents 
Time spent total : ~173.6436 Seconds # versus with RandomAgent
Time spent total : ~317.7048 Seconds # with depth 5 and limit 1000
Time spent total : ~194.9124 Seconds # with depth 4 and limit 10000
```
**Result จริงๆแล้วนะ**
|Limit<br> (α,β)|Depth|Time Spent<br> Second(s)|Agent|
|:---:|:---:|:---:|:---:|
|-2080,2080|4|~100.6128 - 180.4286|Pooh Agent|
|-2080,2080|4|~173.6436|RandomAgent|
|-1000,1000|5|~317.7048|RandomAgent|
|-10000,10000|4|~194.9124|RandomAgent|


เราเจอผลลัพธ์บางอย่างในการรันแต่ละครั้งพบว่าเมื่อ AI คิดได้แล้วแต่ไม่สามารถลงค่าได้ จะไปเข้า Condition ของ except ใน try/except ตรงนี้<br>After I run this code, I found some case that i never expect, My code AI cannot place the value in the board(Place same value) and into except from Try/Except
```python
except Exception as e:
            print(type(e).__name__, ':', e)
            print('search() Traceback (most recent call last): ')
            traceback.print_tb(e.__traceback__)
```
ทำให้ถูก skip turn ไปเนื่องจากลงหมากทับกับตาที่แล้ว<br>That's why my AI is always skip the turn playing after board get full score

### ข้อสังเกต 

เมื่อเราลด limit ลงจะทำให้เราต้องเพิ่ม depth มากขึ้นซึ่งโอกาสโดน skip turn มีสูงมากที่ทำให้เกิดโอกาสแพ้ได้สูงยิ่งขึ้นเช่นกัน<br> เราจะต้องใช้การ prunning เพื่อตัด depth ที่สูงเกินความจำเป็นและกลับมาที่ depth เริ่มต้น ประมาณ 1 - 4 (0 จะไม่มีความลึกของ node) ซึ่งค่าที่เราได้ทั้ง Depth, Level, Limit ตอนนี้ Result ที่ดีที่สุดอยู่ที่ Limit XXXX , Depth X , Level X (หาไม่เจอ555) ยังต้องเพิ่ม Logic อีกหน่อยนึง<br>When we decrease the Limit value we should to increase depth value instead, Chance of skip turn to playing the Othello is very high which will cause the opportunity to even more, so we need to use prunning to cut off the depth of tree and came back to first depth (depth size around 1 - 4)   