# HW 3 Cart-Pole game AI (Auto Mode)

## มี 2 TODO ที่ต้องทำ
    1.  def hillclimb_sideway(env, agent, max_iters=10000, sideway_limit=0):
    เป็นฮิวริสติกฟังก์ชันที่ช่วยในการหาค่าที่ดีที่สุดสำหรับแต่ละสถานการณ์ โดยไม่สนใจค่าที่แย่ที่สุด(เก็บไว้พิจารณาทีหลัง) โดยจำลองจากการปีนเขาโดยให้หาจุดของยอดเขาก่อน โดยให้หาทางที่เร็วที่สุด(หาทิศทางที่ยิ่งปีนยิ่
    ใกล้มากขึ้น) **สิ่งที่ต้องทำคือ ทำให้ hillclimb สามารถขยับได้**
    2.  def simulated_annealing(env, agent, init_temp=25.0, temp_step=-0.1, max_iters=10000):
    เป็นอัลกอริทึ่มที่แก้ปัญหาเพื่อเอาผลลัพธ์มาเฉพาะจุดๆนั้นทำงานแบบวนซ้ำเพื่อหาผลลัพธ์ไปเรื่อยๆจนกว่าจะได้คำตอบที่ดีที่สุด โดยเริ่มจากจุดเริ่มต้น


### ก่อนจะเขียนเราต้อง import อะไรมาใช้บ้าง
```python
import sys

import numpy as np # เป็นโมดูลส่วนเสริมของ Python ที่มีฟังก์ชัน เกี่ยวกับคณิตศาสตร์และการคำนวณต่างๆ มาให้ใช้งาน
import gym # คือชุดเครื่องมือที่ใช้เปรียบเทียบและพัฒนาอัลกอริทึ่มให้ดียิ่งขึ้น
```
### ติดตั้ง Gym OpenAI

เปิด Anaconda Prompt ขึ้นมาเพื่อทำการติดตั้งจากนั้นพิมพ์คำสั่งนี้ลงใน Anaconda Prompt
```bash
    pip install gym
```
แล้วกด Enter เครื่องจะเริ่มทำการติดตั้ง(ต่ออินเทอร์เน็ตด้วย)


### 1. def hillclimb_sideway(env, agent, max_iters=10000, sideway_limit=0):
```python
"""
    Run a hill-climbing search, and return the final agent.

    Parameters
    ----------
    env : OpenAI Gym Environment.
        A cart-pole environment for the agent.
    agent : CPAgent
        An initial agent.
    max_iters: int
        Maximum number of iterations to search.
    sideway_limit
        Number of sideway move to make before terminating.
        Note that the sideway count reset after a new better neighbor
        has been found.

    Returns
    ----------
    final_agent : CPAgent
        The final agent.
    history : List[float]
        A list containing the scores of the best neighbors of 
        all iterations. It must include the last one that causes
        the algorithm to stop.

    """
    cur_agent = agent
    cur_r = simulate(env, [agent])[0]

    explored = set()
    explored.add(cur_agent)
    history = [cur_r]
    
    for __ in range(max_iters):
        # TODO 1: Implement hill climbing search with sideway move.
        pass
    return cur_agent, history
```

### 2. def eightPuzzleH2(state, goal_state):
```python
       """
    Run a hill-climbing search, and return the final agent.

    Parameters
    ----------
    env : OpenAI Gym Environment.
        A cart-pole environment for the agent.
    agent : CPAgent
        An initial agent.
    init_temp : float
        An initial temperature.
    temp_step : float
        A step size to change the temperature for each iteration.
    max_iters: int
        Maximum number of iterations to search.

    Returns
    ----------
    final_agent : CPAgent
        The final agent.
    history : List[float]
        A list containing the scores of the sampled neighbor of 
        all iterations.

    """:
    cur_agent = agent
    cur_r = simulate(env, [agent])[0]
    history = [cur_r]
    sideway = 0

    for __ in range(max_iters):
        # TODO 2: Implement simulated annealing search.
        # We should not keep track of "already explored" neighbor.
        pass
    

    return cur_agent, history
```

