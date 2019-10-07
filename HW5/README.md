# HW5 AI Machine Learning

## Due Date : Monday, 14 October 2019, 11:55 PM

## มี 4 TODO ที่ต้องทำ
    1.  def load_data(): เป็นฟังก์ชันที่เราจะต้องสร้างชุดข้อมูล(เกรด)เพื่อมาใช้ training
    2.  def train(features,labels): ฟังก์ชัน training จะเอา data จาก load_data() มาใช้ในการ train 
    3.  def predict(model,features): ฟังก์ชันนี้จะทำการทำนายความน่าจะเป็นหรือการ predict ค่าจากฟังก์ชัน train
    4.  def evaluate(labels,predictions,label_types): ฟังก์ชันสุดท้ายจะแสดงค่าในรูปแบบ เมทริกซ์ที่บอกค่าความแม่นยำ (confusion matrix) ที่มี

## มีอะไร import มาให้แล้วบ้าง

```python
import numpy as np # ใช้สำหรับการคิดเลขทางคณิตศาสตร์
from sklearn.tree import DecisionTreeClassifier # ใช้สำหรับการ training data 
from sklearn.model_selection import train_test_split # ใช้ sprit หรือแบ่งข้อมูลออกเป็นส่วนๆ
```

## เราต้องติดตั้งอะไรบ้าง

    1. Scikit-Learn โมดูลสำหรับการทำ machine learning

## ติดตั้ง Scikit-Learn

เปิด Anaconda Prompt ขึ้นมาจากนั้นพิมพ์คำสั่งนี้เพื่อติดตั้ง Scikit-Learn
```bash
pip install -U scikit-learn
```
หรือติดตั้งโดยใช้ conda จาก Anaconda Prompt ก็ได้

```bash
conda install scikit-learn
```

### 1. def load_data():

```python
def load_data():
    """
    Return dataset for classification in a form of numpy array.

    The dataset should be in a 2D array where each column is a feature
    and each row is a data point. The last column should be the label.
    
    Your data should contain only number. 
    If you have a categorical feature,  you can replace your feature with 
    "one-hot encoding". For example, a feature 'grade' of values: 
    'A', 'B', 'C', 'D', and 'F' can be replaced with 5 features:
    'is_grade_A', 'is_grade_B', ..., and 'is_grade_F'.

    For the label, you can replace them with 0, 1, 2, 3, ...

    Returns
    -----------
    dataset : np.array
        2D array containing features and label.
```

ฟังก์ชันนี้เราจะต้องสร้าง dataset ขึ้นมา ยิ่ง dataset มีปริมาณมากค่าความแม่นยำในการ training จะยิ่งมากขึ้นตามเช่นกัน โดยในแต่ละ array จะมี 4 ค่าตามตัวอย่างของอาจารย์

```python
    # The following example is a dataset about 
    # quiz, hw, reading hours and grade.
np.array([
        [5, 15, 10, 4],  # 4 is A
        [5, 13, 7, 3],  # 3 is B
        [4, 10, 3, 2],  # 2 is C
        [3, 0, 4, 1],  # 1 is D
        [2, 1, 1, 0],  # 0 is F
        [5, 11, 8, 3],
        [3, 9, 4, 3],
        [5, 6, 3, 2],
        ])
```
Dataset ตัวอย่างของอาจารย์นั้นประกอบไปด้วยค่า 4 ค่าในแต่ละ array คือ

1. Quiz
2. Homework
3. Reading Hours
4. Grade

ฟังก์ชันนี้จะรีเทิร์นค่าออกมาเป็น อาเรย์(Array) ตามที่เราสร้างเพื่อนำไป train data ต่อไป

ตัวอย่าง

```python
def load_data():
    dataset = np.array([
        [5, 15, 10, 4],  # 4 is A
        [5, 13, 7, 3],  # 3 is B
        [4, 10, 3, 2],  # 2 is C
        [3, 0, 4, 1],  # 1 is D
        [2, 1, 1, 0],  # 0 is F
        [5, 11, 8, 3],
        [3, 9, 4, 3],
        [5, 6, 3, 2],
        ])
    return dataset
```

หรือแบบนี้ก็ได้

```python
def load_data():
    return np.array([
        [5, 15, 10, 4],  # 4 is A
        [5, 13, 7, 3],  # 3 is B
        [4, 10, 3, 2],  # 2 is C
        [3, 0, 4, 1],  # 1 is D
        [2, 1, 1, 0],  # 0 is F
        [5, 11, 8, 3],
        [3, 9, 4, 3],
        [5, 6, 3, 2],
        ])
```

### 2. def train(features,labels):

```python
def train(features, labels):
    """
    Return a decision tree model after "training".

    For more information on how to use Decision Tree, please visit
    https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html

    Returns
    ---------
    tree : sklearn.tree.DecisionTreeClassifier

    """
```

ฟังก์ชันนี้จะนำค่าจาก load_data เข้ามาทำการเรียนรู้โดยใช้การตัดสินใจแบบต้นไม้
เราสามารถเอา DecisionTreeClassifier เอามาใช้ training ได้เลย

```python
def train(features, labels):
    return DecisionTreeClassifier().fit(features,labels)
```

หรือ

```python
def train(features, labels):
    train_data = DecisionTreeClassifier()
    return train_data.fit(features,labels)
```

fit() คือการ training data ถ้าเอาให้เข้าใจคือการจับข้อมูลโมเดลมาทำให้ขนาดพอดีกับการ training data<br>

### 3. def predict(model,features): 

```python
def predict(model, features):
    """
    Return the prediction result.

    Parameters
    --------
    model : sklearn.tree.DecisionTreeClassifier
    features : np.array

    Returns
    -------
    predictions : np.array

    """
```

ฟังก์ชั่นนี้จะทำการแสดงคำทำนายหรือค่าความแม่นยำหลังจากที่ใช้ DecisionTreeClassifier หรือการตัดสินใจแบบต้นไม้โดยการแตกกิ่ง

```python
def predict(model, features):
    return model.predict(features) 
```

หรือ

```python
def predict(model, features):
    predict_result = model
    return predict_result.predict(features)
```

การที่เราเอา model.predict เปรียบได้แบบนี้

```python
    model = tree # ที่เราจะเอามา predict 
    # ส่วน features = training_data ที่เราเอามาใช้ฝึก data นั่นเอง
```

### 4. def evaluate(labels, predictions, label_types):

```python
def evaluate(labels, predictions, label_types):
    """
    Return the confusion matrix.

    Parameters
    ---------
    labels : np.array
    predictions : np.array
    label_types : np.array
        This is a list that keeps unique values of the labels, so that
        the confusion matrix has the same order.

    Returns
    ---------
    confusion_matrix : np.array
        The array should have the shape of [# of classes, # of classes].
        Number of class is the length of `label_types`.

    """
    # You can use a library if you can find it.
```

ฟังก์ชั่นนี้จะสร้าง Confusing Matrix ออกมาจาก Training Data และ Testing Data ที่เราได้ทำการ predict ไว้แล้ว ซึ่งฟังก์ชั่นนี้สามารถใช้ Library ได้นั่นก็คือ

```python
from sklearn.metrics import confusion_matrix # Use instead create method to print result
```
confusion_matrix ที่ import จาก scikit-learn 
เขียนโดยใช้ library จะได้แบบนีั

```python
def evaluate(labels, predictions, label_types):
    return confusion_matrix(labels, predictions, label_types)
```

## อธิบายการทำงานของ main ฟังก์ชัน 

```python
if __name__ == "__main__":
    data = load_data() # สร้างตัวแปรมาเพื่อเรียกฟังก์ชัน
    all_labels = data[:, -1] # สร้างตัวแปรมาเพื่อทำการเลือกค่าจากอาเรย์ตัวท้ายที่สุด
    """
    [:,-1] โดย : คือการมองหาค่าทั้งหมดในอาเรย์ ส่วน,-1 คือการ offset โดยเมื่อทำการมองค่าหมดแล้วจะเลือกค่าตัวสุดท้าย
    โดยให้มองค่าเป็นวงกลม
     0  1  2  3 
    [1][2][3][4]

    [:,-1] จะกลายเป็น
    -1  0  1  2  
    [1][2][3][4]  ค่าที่ตำแหน่ง -1 [1] นั้นยังมีค่าอยู่แต่จะมองไม่เห็น ซึ่งจะเห็นค่าแค่ตำแหน่ง 0[2] 1[3] 2[4] ซึ่งเราจะหยิบค่า 4 จาก array ตำแหน่งสุดท้าย

    """
    all_labels = set(all_labels) # แปลงค่าให้อยู่ในรูปของ set
    all_labels = np.array([v for v in all_labels]) # ใช้ loop ในการ print result ออกมาใส่ array
    train_data, test_data = train_test_split(data,test_size=0.3) # แบ่งข้อมูลให้เล็กลง
    features = train_data[:, :-1]
    labels = train_data[:, -1]
    tree = train(features, labels)

    predictions = predict(tree, features)
    print('Training Confusion Matrix:')
    print(evaluate(labels, predictions, all_labels))
    # return value from expression that's equal to labels(array)
    # evaluate(expression, globals=None, locals=None)
    """
    expression - this string as parsed and evaluated as a Python expression
    globals (optional) - a dictionary
    locals (optional)- a mapping object. Dictionary is the standard and commonly used mapping type in Python.
    """
    predictions = predict(tree, test_data[:, :-1])
    print('Testing Confusion Matrix:')
    print(evaluate(test_data[:, -1], predictions, all_labels))

```