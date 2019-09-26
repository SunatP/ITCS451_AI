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
J not in {"a", "c"} # J จะไม่ทำงาน a กับ c นั่นคือถ้ามีงาน a,c,h,i J จะทำงาน h กับ i ได้เท่านั้น
S = I #  S และ I ทำงานเดียวกันได้
H = M #  H และ M ทำงานเดียวกันได้
T != "h" #  T จะไม่ทำงาน h
K = I #  K และ I ทำงานเดียวกันได้
I in {"h", "a"} #  I ทำงานได้แค่ h กับ a
K != H #  K และ H จะไม่ทำงานด้วยกัน
M = "i" #  M จะทำงานได้แค่ i
```

You will solve this by using backtracking search with MAC as the inference 
and MRV for variable ordering. Please answer the following questions:

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
2. H ทำงานร่วมกับ H แต่ M ทำงานได้แค่ i นั่นคือ H กับ M จะทำงาน i ได้อย่างเดียว
3. J จะไม่ทำงาน a,c นั่นคือ J จะทำงานแค่ h,i 
4. J จะไม่ทำงานกับ M โดยที่ M ทำงาน ได้แค่ i ส่วน J ทำได้แค่ h,i นั่นคือ J จะทำได้แค่งาน h เท่านั้น 
5. H จะไม่ทำงานร่วมกับ K ซึ่ง H ทำได้แค่งาน i ทำให้ K ทำงานได้แค่ a,c,h
6. J ไม่ทำงานกับ K และ H ไม่ทำงานกับ K ซึ่ง J ทำได้แค่ h ส่วน K ทำงานได้แค่ a (เนื่องจาก I ทำงานได้แค่ a,h ซึ่งทำให้งาน c,i ต้องโดนตัดทิ้งไป) 
7. K กับ I ซึ่งทำงานด้วยกันจะทำงานได้แค่ a
8. เช่นเดียวกับ S จะทำงานได้แค่ a
9. T จะเป็นอิสระไม่ยุ่งเกี่ยวกับใคร แต่จะไม่ทำงาน h

ภาพที่ได้จากการวิเคราะห์จะเป็นแบบนี้

![After](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/HW4/img/HW4.jpg)

1. How many possible complete states?<br>
Answer: $4^7$ 