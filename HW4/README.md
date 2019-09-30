# HW4 AI 

## Due Date : Sunday, 29 September 2019, 11:55 PM

## Description 

[Project Management] In this semester, you are overwhelmed with group projects.<br> Currently, there are 4 projects under an imminent deadline: <br>

{a, c, h, i} 

Fortunately, you have 7 friends in your group that are ready at your service: 

{H, I, J, K, M, S, T} 

ตีความเรื่อง there are 4 projects under an imminent deadline ก่อน {a,c,h,i} โปรเจคคือ ***Domain***

you have 7 friends in your group that are ready at your service เพื่อน 7 คน {H, I, J, K, M, S, T} คือ ***Variable***

Your job is to assign a project to each of them without 
anyone being free (except you). However, your friends are pretty strange and they want the following constraints to be satisfied:

```bash
S = K #  S and K must work on the same project..
K != J #  K and J do not get along at all.
M != J #  M and J do not get along at all.,
J not in {"a", "c"} # J cannot work on a or c project.
S = I #  S and I must work on the same project.
H = M #  H and M must work on the same project..
T != "h" #  T cannot work on h project.
K = I #  K and I must work on the same project.
I in {"h", "a"} #  I can only work on h and a project.
K != H #  K and H do not get along at all.
M = "i" #  M must work on i project.
```
ตีความ
```bash
S = K #  S และ K ทำงานเดียวกันได้
K != J #  K และ J จะไม่ทำงานด้วยกัน
M != J #  M และ J จะไม่ทำงานด้วยกัน
J not in {"a", "c"} # J จะไม่ทำงาน a กับ c นั่นคือถ้ามีงาน a,c,h,i J จะทำงานได้แค่ h กับ i เท่านั้น
S = I #  S และ I ทำงานเดียวกันได้
H = M #  H และ M ทำงานเดียวกันได้
T != "h" #  T จะไม่ทำงาน h
K = I #  K และ I ทำงานเดียวกันได้
I in {"h", "a"} #  I ทำงานได้แค่ h กับ a
K != H #  K และ H จะไม่ทำงานด้วยกัน
M = "i" #  M จะทำงานได้แค่ i
```

You will solve this by using backtracking search with MAC as the inference 
and MRV for variable ordering. Please answer the following questions:()

1. M จะทำงานได้แค่งาน i
2. H จะทำงานร่วมกับ M 
3. เราจะจับ H กับ M มาอยู่ด้วยกัน
4. M กับ J จะไม่ทำงานด้วยกัน
5. J กับ K จะไม่ทำงานด้วยกัน
6. H กับ K จะไม่ทำงานด้วยกัน
7. จับ J กับ K มาอยู่ด้วยกัน
8. จับ K กับ H มาอยู่ด้วยกัน
9. K กับ S ทำงานร่วมกันได้
10. K กับ I ทำงานร่วมกันได้
11. S กับ I ทำงานร่วมกันได้
12. K กับ S และ I จะทำงานร่วมกันได้ เราจะจับทั้ง 3 มาอยู่ด้วยกัน
13. T จะไม่ทำงาน h

ลองเขียนแผนภาพคร่าวๆจะได้ประมาณแบบนี้

![Before](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/HW4/img/HW4(1).jpg)

วิเคราะห์เรื่องการให้งานกับนักเรียนแต่ละคน
1. M ทำแค่งาน i หมายความว่างาน a,c,h จะไม่ทำ 
2. H ทำงานร่วมกับ M แต่ M ทำงานได้แค่ i นั่นคือ H กับ M จะทำงาน i ได้อย่างเดียว
3. J จะไม่ทำงาน a,c นั่นคือ J จะทำงานแค่ h,i 
4. J จะไม่ทำงานกับ M โดยที่ M ทำงาน ได้แค่ i ส่วน J ทำได้แค่ h,i นั่นคือ J จะทำได้แค่งาน h เท่านั้น 
5. H จะไม่ทำงานร่วมกับ K ซึ่ง H ทำได้แค่งาน i ทำให้ K ทำงานได้แค่ a,c,h
6. J ไม่ทำงานกับ K และ H ไม่ทำงานกับ K ซึ่ง J ทำได้แค่ h ส่วน K ทำงานได้แค่ a (เนื่องจาก I ทำงานได้แค่ a,h ซึ่งทำให้งาน c,i ต้องโดนตัดทิ้งไป) 
7. K กับ I ซึ่งทำงานด้วยกันจะทำงานได้แค่ a
8. เช่นเดียวกับ S จะทำงานได้แค่ a
9. T จะเป็นอิสระไม่ยุ่งเกี่ยวกับใคร แต่จะไม่ทำงาน h

ภาพที่ได้จากการวิเคราะห์จะเป็นแบบนี้

![After](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/HW4/img/HW4.jpg)

<br>
1. How many possible complete states?<br>
<b>Answer: 4 ยกกำลัง 7 (4^7) = 16384 เนื่องจากมี 4 งาน ต้องแบ่งให้นักเรียนให้ครบทั้งหมด 7 คนโดยที่งานไม่ซ้ำกัน</b><br>
1. What is the depth level of the goal state (level 0 means empty assignment)?<br>
<b>Answer: 7 level เนื่องจากใช้ backtracking search เพื่อหาค่าครบทั้ง 7 neighbor โดยใช้ MAC และ MRV เช้ามาช่วย</b><br>
1.  Before we begin running backtracking search, it is much more efficient to eliminate values that invalidate the unary contraints. Please list variables and possible values left after enforcing the unary constrains. Please order your variables and values alphabetically in the following format:<br>
   
```bash
    {
        'VAR1': ['VAL1', 'VAL2'],
        'VAR2': ['VAL2', 'VAL4'],
        ...
        'VAR7': ['VAL2']
    }
```

Such that you can use eval() function to read your answer.<br>
Answer: อ่านจาก following constraints to be satisfied แล้วตีความหมายจะได้ประมาณนี้<br>
```bash
H : {a,c,h,i} # ไม่มี condition
I : {h,a} # I in {"h", "a"} คือ I ทำงานได้แค่ h กับ a
J : {h,i} # J not in {"a", "c"} คือ J จะไม่ทำงาน a กับ c นั่นคือถ้ามีงาน a,c,h,i ซึ่ง J จะทำงานได้แค่ h กับ i เท่านั้น
K : {a,c,h,i} # ไม่มี condition
M : {i} # M = "i" คือ M จะทำงานได้แค่ i
S : {a,c,h,i} # ไม่มี condition
T : {a,c,i} # T != "h" คือ T จะไม่ทำงาน h
```

<b>answer</b>
```bash
    {
        'H': ['a', 'c', 'h', 'i'],
        'I': ['a', 'h'],
        'J': ['h', 'i'],
        'K': ['a', 'c', 'h', 'i'],
        'M': ['i'],
        'S': ['a', 'c', 'h', 'i'],
        'T': ['a', 'c', 'i']
    }
```

<br>
4. Starting from the answer from question 3, please write the assignment you choose to make and the remaining values of all variable in the same format as in question 3. For example,<br>
   
    #ITERATION 1 
    {'VAR1': 'VAL2'} 
    {
        'VAR1': ['VAL2'],
        'VAR2': ['VAL4'],
        ...
        'VAR7': ['VAL2']
    }
    #ITERATION 2
    ...

NOTE: If there is a need to backtrack (MAC detects a failure), it is either the question is incorrect or you are doing it wrong. Please consult me or your classmates. <br>
การเช็ค **Iteration** ทีละตัวทำได้ดังนี้
```bash
    iteration=1 # i = 1 เราจะใช้ MRV มาช่วยเลือก Domain ที่น้อยที่สุดให้กับ Variable ซึ่ง M นั้นมีแค่ i ซึ่งเป็น Domain เดียว
    
        M => i # เครื่องหมาย => คือการ assign เช่น M => i คือ การ assign งาน i ให้ M
        _______
        H -> M => i # เช็ค Neighbor H ที่ไปหา M ซึ่ง H ทำงานกับ M โดยที่ M ทำได้แค่งานเดียว (assign i) ซึ่ง  M และ H ทำงาน i เหมือนกัน ตรงนี้ถูกต้อง
        J -> M => h  # เช็ค Neighbor J ที่ไปหา M ซึ่ง J ไม่ทำงานร่วมกับ M ซึ่ง M ทำได้แค่งาน i ส่วน J ทำงาน h เราจึงต้องเช็ค neighbor of neighbor อีกที (MAC)
        K -> H # เช็ค neighbor ที่มาจาก neighbor H ซึ่ง K มาจาก M แบบนี้ K -> H -> M โดย K จะไม่ทำงานร่วมกับ H โดยที่ K มี assign a ส่วน H นั้นมีแค่ assign i ซึ่งเป็น consistence 
        K -> J # เช็ค neighbor ที่มาจาก neighbor J ซึ่ง K มาจาก J แบบนี้ K -> J -> M โดย K จะไม่ทำงานร่วมกับ J โดยที่ K มี assign a ส่วน J นั้นมีแค่ assign h ซึ่งเป็น consistence 
        # การเช็ค K-> H และ K-> J เป็นการเช็คด้วย MAC หรือ neighbor of Neighbor 
    ___________________________________________________
    # จบ Iteration 1
    iteration=2 # i = 2 เราจะใช้ MRV มาช่วยเลือก Domain ที่น้อยที่สุดให้กับ Variable ซึ่ง H นั้นมีแค่ i ซึ่งเป็น Domain เดียวเหมือนกับ M
        H => i
        ______
        K -> H # เช็ค neighbor ที่มาจาก neighbor H ซึ่ง K มาจาก M แบบนี้ K -> H -> M โดย K จะไม่ทำงานร่วมกับ H โดยที่ K มี assign a ส่วน H นั้นมีแค่ assign i ซึ่งเป็น consistence 
        S -> K # เช็ค neighbor ที่มาจาก neighbor H ซึ่ง S มาจาก K แบบนี้ S -> K -> H โดย S จะทำงานร่วมกับ K ซึ่งเป็น consistence 
    
```

<b>Answer: เริ่มจากการใช้ MRV มาทำการตรวจจับ Node ที่มี value น้อยที่สุดก่อนเพื่อ assign งานเข้าก่อนเป็นตัวเริ่ม Iteration จากนั้นก็ไล่งานให้ครบ ทุก Neighbor โดยใช้รูปภาพอ้างอิง</b> <br>
![After](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/HW4/img/HW4.jpg)

```bash
    # ITERATION 1
    {'M': 'i'}
    {
        'H': ['i'],
        'I': ['a'],
        'J': ['h'],
        'K': ['a'],
        'M': ['i'],
        'S': ['a'],
        'T': ['a','c','i']
    }
    # ITERATION 2
    {'H':'i'}
    {
        'H': ['i'],
        'I': ['a'],
        'J': ['h'],
        'K': ['a'],
        'M': ['i'],
        'S': ['a'],
        'T': ['a','c','i']  
    }
    # ITERATION 3
    {'J':'h'}
    {
        'H': ['i'],
        'I': ['a'],
        'J': ['h'],
        'K': ['a'],
        'M': ['i'],
        'S': ['a'],
        'T': ['a','c','i']
    }
    # ITERATION 4
    {'K':'a'}
    {
        'H': ['i'],
        'I': ['a'],
        'J': ['h'],
        'K': ['a'],
        'M': ['i'],
        'S': ['a'],
        'T': ['a','c','i']   
    }
    # ITERATION 5
    {'S':'a'}
    {        
        'H': ['i'],
        'I': ['a'],
        'J': ['h'],
        'K': ['a'],
        'M': ['i'],
        'S': ['a'],
        'T': ['a','c','i']
    }
    # ITERATION 6
    {'I','a'}
    {
        'H': ['i'],
        'I': ['a'],
        'J': ['h'],
        'K': ['a'],
        'M': ['i'],
        'S': ['a'],
        'T': ['a','c','i']
    }
    # ITERATION 7
    {'T':'c'}
    {
        'H': ['i'],
        'I': ['a'],
        'J': ['h'],
        'K': ['a'],
        'M': ['i'],
        'S': ['a'],
        'T': ['c']        
    }
```