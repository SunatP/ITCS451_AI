# HW 3 Cart-Pole game AI (Auto Mode)

## Due Date Wednesday, 25 September 2019, 11:55 PM

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
```
ตัวอย่าง Pseudo code / Algorithm ของ sideway
```bash
function Hillclimb(Initial,K)
    initialize node with Initial # Set the current node to starting point
    while forever # Continue until you cannot climb higher 
        initialize max to -infinity # Minimum value
        for each child(neighbor) of the node 
            if v(child) > max # Find neighbor with max value
                max = v(child)
                next = child
        if max <= 0 # Cannot climb higher 
            if k == 0
                return node
            for each child(neighbor) of the node
                value = Hillclimb(child,k-1)
                if value > max
                    max = value
                    next = child
            if max <= 0
                return node
        node = next # Climb to the next node
```
เริ่มเขียน TODO 1
```python
def hillclimb_sideway(env, agent, max_iters=10000, sideway_limit=10):
    cur_agent = agent
    cur_r = simulate(env, [agent])[0]

    explored = set()
    explored.add(cur_agent)
    history = [cur_r]

    for __ in range(max_iters):
        # TODO 1: Implement hill climbing search with sideway move.
        # Get All the Neighbors
    return cur_agent, history

```
เริ่มเขียน TODO 1
```python
def hillclimb_sideway(env, agent, max_iters=10000, sideway_limit=10):
    cur_agent = agent
    cur_r = simulate(env, [agent])[0]

    explored = set()
    explored.add(cur_agent)
    history = [cur_r]
    k = 0  # สร้างตัวนี้
    sideScore = 0 # สร้างตัวนี้
    for __ in range(max_iters):
        # สร้าง list ขึ้นมาเพื่อเก็บ neighbor ตัวก่อนหน้านี้
        PreviousNeighbor: list[CPAgent] = cur_agent.neighbors() # ตัวนี้จะมี CPAgent อยู่ใน list ที่คอยหา Neighbors ให้
        # สร้าง list ใหม่ขึ้นมาเพื่อเก็บ neighbor 
        NewNeighbor: list[CPAgent] = []
        for i in PreviousNeighbor: # ใช้ i ในการหา Neighbors
            if i not in explored: # ถ้า i ไม่มีค่า
                NewNeighbor.append(i) # เอา i ที่หาค่าได้ใส่ลงใน list NewNeighbor
            # จบ if condition
        # จบ for loop
        PreviousNeighbor = NewNeighbor # Neighbor ตัวใหม่จะเท่ากับตัวก่อนหน้า
        # สร้างตัวแปรมาคำนวน Reward
        CalculateReward = simulate(env,PreviousNeighbor) # ใช้ env ที่มี gym มาคำนวนค่าด้วย Neighbor ก่อนหน้า
        history.append(Calculate[np.argmax(Calculate)]) # ค่าที่คำนวนหา value ที่มากที่สุดจาก gym จะถูกใส่ลงใน list ชื่อ history
        BestValue = CalculateReward[np.argmax(Calculate)] # สร้างขึ้นเพื่อหาค่าที่ดีที่สุดและมากที่สุด
        MaxValue = PreviousNeighbor[np.argmax(CalculateReward)] # สร้างมาเพื่อหา Neighbor ตัวก่อนหน้าที่มีค่ามากที่สุด
        if BestValue < simulate(env, [agent])[0]: # ถ้าค่าที่หาได้น้อยกว่าขณะกำลังปีนขึ้นเขา
            return MaxValue, history # เราจะใช้ค่าที่มากที่สุดแทน
        # จบ if condition
        else:
            if cur_r == CalculateReward[np.argmax(simulate(env,PreviousNeighbor))]: # ถ้าตัวปัจจุบันมีค่าเท่ากับค่าที่สูงที่สุดของ Neighbor ที่เจอค่าตัวก่อนหน้านี้
                if sideScore != CalculateReward[np.argmax(simulate(env,PreviousNeighbor))]: # ถ้าค่า sideScore ไม่เท่ากับค่าของ CalculateReward
                    sideScore = CalculateReward[np.argmax(simulate(env,PreviousNeighbor))] # จับค่า CalculateReward เท่ากับ sideScore
                    k = 0 # เริ่มนับค่า k ใหม่ (รีเซ็ทค่า)
                #จบ if sideScore
                k += 1
                if sideway_limit == k : # ถ้า sideway_limit เท่ากับค่า k 
                    return MaxValue,history
                # จบ if condition
            cur_agent = PreviousNeighbor[np.argmax(simulate(env, PreviousNeighbor))] # ตัวปัจจุบันจะมีค่ามากที่สุดจากตัวก่อนหน้า
            cur_r = CalculateReward[np.argmax(simulate(env, PreviousNeighbor))] # ค่า Reward เท่ากับ ค่าที่คำนวนจาก ค่าที่มากที่สุดจากตัวก่อนหน้า
    # จบ for loop
    return cur_agent, history
```

### 2. def simulated_annealing(env, agent, init_temp=25.0, temp_step=-0.1, max_iters=10000):

simulated_annealing หรือ การจำลองการอบเหนียว

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
```

ตัวอย่าง Pseudo code / Algorithm ของ Simulated-Annealing

```bash
function Simulated-Annealing(problem,schedule) return a solution state
Input problem, a problem schedule, a mapping from time to "temperature"

current <- MAKE-NODE(problem.INITIAL-STATE)
for t = 1 to inf.
    T <- schedule(t) # อุณหภูมิ ณ ตอนนั้น
    if T <= 0 then return current
    next <- a randomly selected successor of current # ค่าตัวถัดไปคือการสุ่มค่าจากตัวปัจจุบัน
    DeltaEnergy <- next.VALUE - current.VALUE # ตัวถัดไป ลบด้วย ตัว node ปัจจุบัน
    if DeltaEnergy > 0 then current <- next
    else current <- next only with probability e^(DeltaEnergy/T) # e คือ exponential , eยกกำลัง(DeltaEnergyหารด้วยT)
```
อัลกอริทึมตัวนี้จะจำลองสภาพการแก้ปัญหาเหมือนการหลอมเหล็กและค่อยๆลดอุณหภูมิลงโดยทำให้เหล็กนั้นมีสภาพแข็งขึ้นไม่เปราะหรือแตกหักได้ง่าย

```python
def simulated_annealing(env, agent, init_temp=25.0, temp_step=-0.1, max_iters=10000):
     cur_agent = agent
    cur_r = simulate(env, [agent])[0]
    history = [cur_r]
    sideway = 0

    Temp = init_temp # สร้างตัวแปรขึ้นมาเก็บค่าอุณหภูมิเริ่มต้น
    for __ in range(max_iters):
        Temp += temp_step # ค่า Temp จะลดลงไปเรื่อยๆ เนื่องจาก temp_step มีค่า -0.1 นั่นก็คือการลดอุณหภูมิ
        if Temp <= 0 :# ถ้าอุณหภูมิลดลงจนน้อยกว่า 0
            break # จบการทำงานของ for loop
        #จบ if condition
        PreviousNeighbor: list[CPAgent] = cur_agent.neighbors() # ใช้หา neighbor ตัวก่อนหน้า
        NextNeighbor: CPAgent = np.random.choice(PreviousNeighbor,1)[0] # Neighbor ตัวถัดคือความน่าจะเป็นที่สามารถเลือกได้
        cur_r = simulate(env,[cur_agent])[0] # ใช้ gym มาจำลองค่าใน Current Reward
        E = simulate(env, [Next])[0] - cur_r # E หรือ DeltaE คือพลังงานที่เกิดจาก ค่าของตัวถัดไปลบด้วย ค่าปัจจุบัน
        if E > 0 :
            cur_agent = NextNeighbor # ค่าของตัวถัดไปจะเท่ากับตัวปัจจุบัน
            cur_r = simulate(env, [cur_agent])[0] # ค่า Reward ปัจจุบันจะเท่ากับ agent ตัวปัจจุบัน
        # จบ if condition
        else:
            if np.random.normal()<= pow(math.e, E/Temp): # ถ้าการสุ่มค่าแบบปกติ นั้นมีค่าน้อยกว่า exponential ยกกำลัง E/Temp
                cur_agent = NextNeighbor
                cur_r = simulate(env, [cur_agent])[0]]
        history.append(cur_r) # ใส่ current Reward ลงใน history
    return cur_agent, history
```

### วิธีรันโค้ด

1. รันแบบปกติ
2. รันแบบใช้ Terminal/Command Prompt/PowerShell

1. รันแบบปกติ โดยใช้ VSCode

   1. มองหาโค้ดหน้าตาแบบนี้ จะอยู่ล่างสุด
```python
if __name__ == "__main__":
    gym.envs.register(
        id='CartPole-v2',
        entry_point='gym.envs.classic_control:CartPoleEnv',
        max_episode_steps=1500,
        reward_threshold=1500.0
    )
    env = gym.make('CartPole-v2')
    # w1 = np.array([-0.0723, -0.0668, 0.151, 0.0802])
    # b1 = np.array([-0.0214])
    if len(sys.argv) > 1:
        if sys.argv[1] != 'random':
            _w = [float(v.strip()) for v in sys.argv[1].split(',')]
            w1 = np.array(_w[:4])
            b1 = np.array(_w[4:5])
            agent = CPAgent(w1=w1, b1=b1)
        else:
            agent = CPAgent()
        print(agent)
        env.seed(42)
        obs = env.reset()
        total_reward = 0
        for t in range(1500):
            env.render()
            action = agent.act(obs)
            obs, reward, done, info = env.step(action)
            total_reward += reward
            # if done:
            #     break
        
        print('Total Reward: ', total_reward)
    else: 
        agent = CPAgent()
        # Hill Climbing search can solve this case.
        # agent = CPAgent(w1=np.array([0.0111, 0.0909, 0.0688, 0.189]), b1=np.array([0.0456]))
        # Hill Climbing search cannot solve this case, but sideway move limit at 10 will solve this.
        # agent = CPAgent(w1=np.array([0.0155, 0.0946, 0.0225, 0.0975]), b1=np.array([-0.0628]))
        initial_reward = simulate(env, [agent])[0]
        print('Initial:    ', agent, ' --> ', f'{initial_reward:.5}')
        agent, history = hillclimb(env, agent)
        initial_reward = simulate(env, [agent])[0]
        for score in history:
            print(score)
        print('After:      ', agent, ' --> ', f'{initial_reward:.5}')
        
        neighbors = agent.neighbors()
        rewards = simulate(env, neighbors)
        for i, (a, r) in enumerate(zip(neighbors, rewards)):
            print(f'Neighbor {i}: ', a, ' --> ', f'{r:.5}')
    env.close()
    
```
   2. มองหาที่ else จะมีถ้าเจอ agent = CPAgent() อยู่ ให้คลิกขวา แล้วกด Run Python File in Terminal 
```python
else: 
    # agent = CPAgent()
    # agent,history = hillclimb_sideway(env,CPAgent(w1=np.array([0.0011, 0.0909, 0.0688, 0.189]), b1=np.array([0.0456]))) # Test hillclimb sideway
    agent,history = simulated_annealing(env,CPAgent(w1=np.array([0.0111, 0.0909, 0.0688, 0.189]), b1=np.array([0.0456]))) # Test annealing
    # Hill Climbing search can solve this case.
    # agent = CPAgent(w1=np.array([0.0111, 0.0909, 0.0688, 0.189]), b1=np.array([0.0456]))
    # agent = CPAgent(w1=np.array([0.0011, 0.0909, 0.0688, 0.189]), b1=np.array([0.0056])) # Hill climbing search can solve this case Total Reward is 1500
    # Hill Climbing search cannot solve this case, but sideway move limit at 10 will solve this.
    # agent = CPAgent(w1=np.array([0.0155, 0.0946, 0.0225, 0.0975]), b1=np.array([-0.0628]))
       
```
   3. ที่ agent = CPAgent() จะมีคอมเม้นของอาจารย์เพิ่มอีกสองค่า โดยคอมเม้นแรกบอกว่า Hill Climbing Search สามารถแก้ปัญหาได้ ให้ทำการเอา # หน้า agent ออกจะได้แบบนี้
```python
    # agent = CPAgent()
    # agent,history = hillclimb_sideway(env,CPAgent(w1=np.array([0.0011, 0.0909, 0.0688, 0.189]), b1=np.array([0.0456]))) # Test hillclimb sideway
    agent,history = simulated_annealing(env,CPAgent(w1=np.array([0.0111, 0.0909, 0.0688, 0.189]), b1=np.array([0.0456]))) # Test annealing
    # Hill Climbing search can solve this case.
    # agent = CPAgent(w1=np.array([0.0111, 0.0909, 0.0688, 0.189]), b1=np.array([0.0456]))
    # agent = CPAgent(w1=np.array([0.0011, 0.0909, 0.0688, 0.189]), b1=np.array([0.0056])) # Hill climbing search can solve this case Total Reward is 1500
    # Hill Climbing search cannot solve this case, but sideway move limit at 10 will solve this.
    # agent = CPAgent(w1=np.array([0.0155, 0.0946, 0.0225, 0.0975]), b1=np.array([-0.0628]))
       
```
   4. จากนั้นคลิกขวาที่โค้ดแล้วกด Run Python File in Terminal จะได้ผลลัพธ์ออกมา

2. รันแบบไม่ปกติ(ใช้ Command Prompt/Terminal/PowerShell)
   1. เปิด Command Prompt ขึ้นมา
![1](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/HW3/img/1.jpg)
   2. เปิดแฟ้มและคัดลอกที่อยู่ของแฟ้มที่เราเก็บโค้ดไว้
![2](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/HW3/img/2.jpg)
   3. พิมพ์ cd แล้วกดวางที่อยู่โฟลเดอร์นั้นๆ แล้วกด Enter
![3](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/HW3/img/3.jpg)
   4. Command Prompt จะเปลี่ยนเป็น Path ของโฟลเดอร์นั้นๆ
   5. พิมพ์ คำสั่งลงไป แล้วกด enter
```bash 
python itcs451-hw3.py "random"
```
ตรงคำว่า random เราสามารถใส่ค่าอื่นได้เช่น
```bash
python itcs451-hw3.py "0.0111, 0.0909, 0.0688, 0.189,0.0456"
```
![4](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/HW3/img/4.jpg)
   6. จะมี Cart-Pole จาก python ขึ้นมาให้รอจนกว่าหน้าต่างนั้นจะหายไปแล้วใน Command Prompt จะมี Total Reward ขึ้นมาเป็นอันจบ  
![5](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/HW3/img/5.jpg)
![6](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/HW3/img/6.jpg)