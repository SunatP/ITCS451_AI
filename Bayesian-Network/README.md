# AI Bayesian Network

## Due Date : Friday, 6 December 2019, 11:55 PM

### What we need to do in this project?

1. Netica [Download Click Here](https://www.norsys.com/downloads/Netica_Win.exe)
2. Bayesian Network Data [Example Click Here](http://www.bnlearn.com/bnrepository/) (recommend select data from small Networks [<20 nodes] or Medium Networks [20 - 50 nodes])
   1.  Example for Small Data [Click Here](http://www.bnlearn.com/bnrepository/discrete-small.html#asia)


### Setup Netica Program

หลังจากโหลดไฟล์ Netica แล้วไม่ต้องติดตั้งไฟล์ ทำตามขั้นตอนตามลำดับดังภาพก็สามารถใช้งานได้แล้ว

1. ไฟล์ที่โหลดมามันจะมีชื่อแบบนี้ เราก็ดับเบิ้ลคลิกไฟล์ตามปกติ
![1](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/1.PNG)
2. มันจะมีหน้าต่างขึ้นมาแบบนี้ตามภาพ ให้เรากด Unzip<br>
![2](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/2.PNG)
3. หลังจากที่กด **Unzip** แล้วตัวแฟ้มตัวนี้จะไปอยู่ที่ ไดรฟ์ C: จะมีแฟ้มชื่อ Netica โผล่มา
![3](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/3.PNG)
![4](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/4.PNG)
ตัวโปรแกรมจะอยู่ในแฟ้ม **C:\Netica\Netica 605** เมื่อเข้ามาในแฟ้มแล้วดับเบิ้ลคลิกที่โปรแกรมชื่อว่า **Netica32** เพื่อทำการเรียกใช้งาน
4.  หลังจากเปิดขึ้นมาแล้วจะมีหน้าตาแบบนี้
![5](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/5.PNG)
ให้เรากดปุ่ม Limited Mode (Limited Mode จะใช้งานได้ไม่เกิน 10 Nodes) เพื่อเข้าใช้งานโปรแกรม เมื่อกดเข้ามาแล้วจะเป็นอย่างงี้
![6](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/6.PNG)
5. ให้เรากด New Net ขึ้นมาจะมีหน้าต่างใหม่ขึ้นมาแบบนี้
![7](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/7.PNG)
6. ต่อมากดที่ปุ่มวงกลมสีเหลือง (Add Nature Node) ตรงนี้ 
![8](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/8.PNG)
7. แล้วมากดตรงที่ว่างในหน้าต่างที่เรากดสร้างใหม่ขึ้นมาจะขึ้นมาดังภาพ
![9](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/9.PNG)
8. ดับเบิ้ลคลิกที่ Nature Node ที่เราวางไว้ตรงพื้นที่ขาวๆ (ในรูปจะมีชื่อว่า A แล้วก็ state0) จะมีหน้าต่างใหม่ขึ้นมา
![10](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/10.PNG) ตรง A เราจะเปลี่ยนชื่อเป็นอะไรก็ได้ ในตัวอย่างเราจะตั้งชื่อเป็น Smoker จากนั้นลงมาดูที่ State เราสามารถเขียน State แบบไหนก็ได้ในตัวอย่างเราจะเขียน True กับ False ลงไป โดยเขียน True ลงไปแล้วกด New 
![11](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/11.PNG)
จากนั้นเราพิมพ์ False ลงไปแต่ไม่ต้องกด New
![12](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/12.PNG)
แล้วให้เรามากดที่ปุ่ม OK จะขึ้นมาตามภาพ
![13](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/smoker.PNG)
เราจะสร้างอีกอันนึงขึ้นมาชื่อว่า Pollution กำหนดค่า Low High ตามนี้
![14](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/13.PNG)
ต่อมาเราจะสร้างอีกอันนึงชื่อว่า Cancer ที่กำหนดค่า True False
![15](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/14.PNG) เมื่อสร้างมาแล้วไปกดที่ปุ่มลูกศร (Add Link) แล้วลากจาก Smoker ไปที่ Cancer และ Pollution ไปที่ Cancer 
![16](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/15.PNG) เมื่อลากแบบนี้ตามภาพแล้วให้กดรูปสายฟ้า (Complie Net) จะมีกราฟแท่งขึ้นมาแบบนี้
![17](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/16.PNG)
จากนั้นคลิกขวาที่ Smoker เลือก Table
![18](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/17.png)
เราจะทำการใส่ค่าลงไปที่ True และ False เป็น 30 กับ 70
![19](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/18.PNG)
ตามภาพนี้เป็นต้น
![20](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/19.PNG)
เมื่อเราใส่เสร็จแล้วก็กด OK อีกอันนึงสำหรับ Pollution เราจะใส่เป็น Low 90 และ High 10 ต่อมาที่ Cancer เราจะคลิกขวาและกด Table ลองแก้ไขโดยใส่ค่าตามภาพ
![21](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/21.PNG)
จากนั้นสร้าง Node ขึ้นมาอีกสองตัวตามภาพ ในภาพเราจะสร้าง XRay 
![22](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/22.PNG)
![23](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/23.PNG)
กับ Dysnopea และใส่ค่าตามภาพ เมื่อใส่ค่าเสร็จแล้วให้ลากลูกศร (Add Link) จาก Cancer มาที่ XRay และ Dysnopea จากนั้นกด Compile Net จะได้ตามภาพดังนี้
![24](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/24.PNG)
จากนั้นลองคลิกที่ True ตรง Cancer ค่าที่ได้จะเปลี่ยนไปทั้งภาพ
![25](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/25.PNG)
ถ้าเราเปลี่ยนเป็นคลิกที่ False ดูบ้างค่าก็จะเปลี่ยนไปเหมือนกัน
![26](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/26.PNG)
ถ้ามากดที่ False ตรง Pollution ค่าก็จะเปลี่ยนไปอีกเช่นกัน
![27](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/27.PNG)
หรือจะตรง Smoker ก็ตาม
![28](https://raw.githubusercontent.com/SunatP/ITCS451_AI/master/img/28.PNG)


### อีกวิธีนึงเร็วกว่านี้อีกเยอะ

1. ให้เราสร้างไฟล์ขึ้นมาใหม่
2. จากนั้นไปที่ Cases -> Learn -> Add Cases File Node...
3. ให้เราหาไฟล์ที่มีนามสกุล .csv ที่มี data ไม่เกิน 10 column
4. จากนั้นจะมีกล่องขึ้นคำถาม How many states would you like continuous node CL to have (0 for no discretization)?