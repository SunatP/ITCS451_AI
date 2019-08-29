# HW 1 8-Puzzle solve without AI (Manual Mode)

## มี 4 TODO ทีต้องทำ

  1.    InitializeState(): ต้องทำให้ฟังก์ชันนี้สุ่มค่ามาในรูปแบบ nested list หรือ 2D-Array หรือ อาเรย์ 2 มิติ
  2.    Successor(): เป็นฟังก์ชันที่ขยับตัว 0 ให้เลื่อนไปปตามตารางของ 8-Puzzle ได้
  3.    is_goal(): ใช้บอกตำแหน่งเคลื่อนที่ได้ตาม self.board โดยให้รีเทิร์นค่ามาเป็น True or False
  4.    trace(): ใช้ระบุการเคลื่อนตำแหน่งของ Tile ว่าเคลื่อนที่ยังไง

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
    # สร้างอาเรย์เปล่าขึ้นมาก่อนชื่ออะไรก็ได้กำหนดค่าให้สูงสุด 9 ค่า คือ ตั้งแต่ 0,1,2,3,4,5,6,7,8
    array = list(range(0,9))
    # เมื่อ

```