# HW 1 8-Puzzle solve without AI (Manual Mode)

## มี 4 TODO ทีต้องทำ

  1.    InitializeState(): ต้องทำให้ฟังก์ชันนี้สุ่มค่ามาในรูปแบบ nested list หรือ 2D-Array หรือ อาเรย์ 2 มิติ
  2.    Successor(): เป็นฟังก์ชันที่ขยับตัว 0 ให้เลื่อนไปปตามตารางของ 8-Puzzle ได้
  3.    is_goal(): ใช้บอกตำแหน่งเคลื่อนที่ได้ตาม self.board โดยให้รีเทิร์นค่ามาเป็น True or False
  4.    trace(): ใช้ระบุการเคลื่อนตำแหน่งของ Tile ว่าเคลื่อนที่ยังไง(-u , -l , -d, -r เป็นต้น)

### 1 InitializeState()
```python
    """
    Create an 8-puzzle state with a SHUFFLED tiles.
        
    Return
    ----------
    EightPuzzleState
        A state that contain an 8-puzzle board with a type of List[List[int]]: 
        a nested list containing integers representing numbers on a board
        e.g., [[0, 1, 2], [3, 4, 5], [6, 7, 8]] where 0 is a blank tile.
    """

```
ฟังก์ชันนี้เป็นการสุ่มค่าอาเรย์สองมิติให้กับ 8-Puzzle 

```python
    # สร้างอาเรย์เปล่าขึ้นมาก่อนชื่ออะไรก็ได้กำหนดค่าให้สูงสุด 9 ค่า คือ ตั้งแต่ 0,1,2,3,4,5,6,7,8 โดยตัวที่กำหนดค่าคือฟังก์ชัน range()
    array = list(range(0,9))
    # เมื่อเราสรา้งอาเรย์เสร็จแล้วให้เราทำการสุ่มค่าโดยใช้ฟังก์ชันสุ่มค่าที่ชื่อว่า shuffle()
    random.shuffle(array) # ตรงนี้เมื่อทุกครั้งที่เรารันโค้ดเลขจะถูกการสุ่มทุกๆครั้งที่โปรแกรมทำงาน
    # สร้างตัวแปรนับค่าอีกตัว
    count = 0
    # จากนั้นให้สร้างอาเรย์เปล่าขึ้นมาอีกตัว
    array2 = [] # นี่คืออาเรย์เปล่าๆ
    # จากนั้นเราสามารถใช้ for loop ได้สองรูปแบบ
```

### for loop แบบที่ 1 ใช้ i,j มาควบคุม
``` python
    for i in range(0,3) # ใช้คุมอาเรย์มิติที่ 1 ได้ตั้งแต่ 0 - 2
        row = [] # สร้างอาเรย์เปล่าอีกที
        for j in range(0,3) # ใช้คุมอาเรย์มิติที่ 2 ได้ตั้งแต่ 0 - 2
        row.append(array[count]) # เอาค่าจาก count ไปใส่ใน array row
        count += 1
    array2.append(row) # อาเรย์ row จะถูกรวมกับ อาเรย์2
    return EightPuzzleState(nestlist)
    pass
```
โค้ดโดยใช้ for loop แบบแรกจะประมาณนี้
```python
    def initializeState():
    # สร้างอาเรย์เปล่าขึ้นมาก่อนชื่ออะไรก็ได้กำหนดค่าให้สูงสุด 9 ค่า คือ ตั้งแต่ 0,1,2,3,4,5,6,7,8 โดยตัวที่กำหนดค่าคือฟังก์ชัน range()
    array = list(range(0,9))
    # เมื่อเราสรา้งอาเรย์เสร็จแล้วให้เราทำการสุ่มค่าโดยใช้ฟังก์ชันสุ่มค่าที่ชื่อว่า shuffle()
    random.shuffle(array) # ตรงนี้เมื่อทุกครั้งที่เรารันโค้ดเลขจะถูกการสุ่มทุกๆครั้งที่โปรแกรมทำงาน
    # สร้างตัวแปรนับค่าอีกตัว
    count = 0
    # จากนั้นให้สร้างอาเรย์เปล่าขึ้นมาอีกตัว
    array2 = [] # นี่คืออาเรย์เปล่าๆ
    # จากนั้นเราสามารถใช้ for loop ได้สองรูปแบบ
    for i in range(0,3) # ใช้คุมอาเรย์มิติที่ 1 ได้ตั้งแต่ 0 - 2
        row = [] # สร้างอาเรย์เปล่าอีกที
        for j in range(0,3) # ใช้คุมอาเรย์มิติที่ 2 ได้ตั้งแต่ 0 - 2
        row.append(array[count]) # เอาค่าจาก count ไปใส่ใน array row
        count += 1
    array2.append(row) # อาเรย์ row จะถูกรวมกับ อาเรย์2
    return EightPuzzleState(nestlist)
    pass
```

### for loop แบบที่สอง(ฉบับรวบรัด)

```python
    def initializeState():
        List = [] # สร้างอาเรย์เปล่าขึ้นมา
        a = random.sample(range(9),9) # ทำการสุ่มค่าทั้งหมด 9 ตัว ตั้งแต่ 0 - 8
        for i in range(0,len(a),3) : # สร้าง for loop มา โดยใช้ range(start,stop,step)
        #โดย range(0,len(a),3) 0 คือค่าเริ่มต้น len(a) คือค่า length ของ a ที่ทำการสุ่มค่า ตัวสุดท้ายคือการ step นับทีละ 3 ตัว
            List.append(c[i:i+3]) # นำค่าไปใส่ในอาเรย์ที่ชื่อ List โดยแบ่งเป็นอาเรย์ที่มีกล่องละ 3 ค่าที่ไม่ซ้ำกัน
        # ตัวอย่าง [[0, 4, 1], [2, 6, 8], [3, 7, 5]]
    return EightPuzzleState(List) # ส่งอาเรย์ที่มีชื่อว่าList (List คืออาเรย์ที่มีค่าพร้อมใช้งานแล้ว)กลับไปที่คลาสชื่อ EightPuzzleState

```


### 2 Successor(self,action):
```python
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
```

เป็นฟังก์ชันควบคุมการเคลื่อนที่ของ Puzzle 
```python
        def Successor(self,action):
        if action not in self.action_space:
            raise ValueError(f'`action`: {action} is not valid.') # ถ้าเราใส่ string ที่ไม่ใช่ u,d,l,r ลงไปจะมี output Error ออกมา

        new_board = copy.deepcopy(self.board) # ใช้สำหรับการคัดลอก object โดยไม่มี Reference เชื่อมโยงกันในหน่วยความจำครับ ดังรูป 
```
![Deepcopy](https://cdncontribute.geeksforgeeks.org/wp-content/uploads/deep-copy.jpg)

เพิ่มโค้ดเพื่อสร้างการควบคุม 8-Puzzle

```python
    # self คือชื่อพารามิเตอร์ตัวแรก ถ้าเป็น java หรือ C จะใช้เป็น this
    NewX = self.x
    NewY = self.y
    if action == 'u' : # ถ้า string ที่ input มาคือ u / up
        NewY = (self.y) - 1
    elif action == 'd': # ถ้า string ที่ input มาคือ d / down
        NewY = (self.y) + 1
    elif action == 'l': # ถ้า string ที่ input มาคือ l / left
        NewX = (self.x) -1
    elif action == 'r': # ถ้า string ที่ input มาคือ r / right
        NewX = (self.x) + 1
    if Newx == -1 or Newy == -1: 
        return None # กรณีที่ 0 อยู่สุดกระดานแล้วเราจะไม่สามารถทำให้มันขยับออกนอกกระดานได้
    if Newx == 3 or Newy == 3:
        return None # กรณีที่ 0 อยู่สุดกระดานแล้วเราจะไม่สามารถทำให้มันขยับออกนอกกระดานได้
    new_board[self.y][self.x]=new_board[NewY][NewX] # นำค่าลงไปทับ
    new_board[NewY][NewX] = 0

    return EightPuzzleState(new_board)
```

โค้ดจะออกมาประมาณนี้

```python
    def Successor(self,action):
        if action not in self.action_space:
            raise ValueError(f'`action`: {action} is not valid.') # ถ้าเราใส่ string ที่ไม่ใช่ u,d,l,r ลงไปจะมี output Error ออกมา

        new_board = copy.deepcopy(self.board)
        NewX = self.x
    NewY = self.y
    if action == 'u' : # ถ้า string ที่ input มาคือ u / up
            NewY = (self.y) - 1
        elif action == 'd': # ถ้า string ที่ input มาคือ d / down
            NewY = (self.y) + 1
        elif action == 'l': # ถ้า string ที่ input มาคือ l / left
            NewX = (self.x) -1
        elif action == 'r': # ถ้า string ที่ input มาคือ r / right
            NewX = (self.x) + 1
        if Newx == -1 or Newy == -1: 
            return None # กรณีที่ 0 อยู่สุดกระดานแล้วเราจะไม่สามารถทำให้มันขยับออกนอกกระดานได้
        if Newx == 3 or Newy == 3:
            return None # กรณีที่ 0 อยู่สุดกระดานแล้วเราจะไม่สามารถทำให้มันขยับออกนอกกระดานได้
        new_board[self.y][self.x]=new_board[NewY][NewX] # นำค่าลงไปทับ
        new_board[NewY][NewX] = 0

    return EightPuzzleState(new_board)
```

### 3 is_goal(self, goal_board=[[1, 2, 3], [4, 5, 6], [7, 8, 0]]):

ใช้เช็คเงื่อนไขว่าเรา Puzzle ที่เราทำถูกหรือไม่

```python
    if self.board == goal_board: # ถ้า self.board เหมือนกันกับ goal_board
        return True # รีเทิร์นค่ากลับไปว่าถูกแล้ว
    else :
        return False  # รีเทิร์นค่ากลับไปว่ายังไม่ถูก
```

### 4 def trace(self):

ใช้บอกว่าเรากดปุ่มไหนไปแล้วบ้างหลังจากโปรแกรมจบหรือกดยกเลิกก่อน

```python
     Nodes = []
        # currentNode = self

        while self.parent is not None:
            Nodes.append(self)
            self = self.parent

        if self.parent is None: # ถ้าเริ่มเกมมาไม่มี Input
            Nodes.append(self)
            self = self.action # ให้เอา Action - INIT ใส่เข้าไป

        Nodes.reverse() # เรียงจาก root node ไปหา current node

        # print(currentNode)
        return Nodes
    pass 
```