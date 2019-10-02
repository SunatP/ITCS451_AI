# # Getting Data Type
# import math
# import os
# import time
# from tqdm import tqdm

# for i in tqdm(range(int(10e6)),ascii= True, desc="Loading"): # Loading bar
#     pass

# x = 5
# y = 'Sunat'
# print('x' + ' =',x , ', Data Type of x :', type(x))
# print('y' + ' =',x , ', Data Type of y :',type(y))
# print(type(math.pi))
# print(type(list(('cat','frog','John'))))
# print(10e6) # 10 power 6
# print(complex(4j))
# time.sleep(3)
# os.system('cls')
# # How to cast a variable

# z = float(12.33)
# print(z)
# print(type(z))
# z1 = str('x1')
# print(z1)
# print(type(z1))
# # 'hello' is the same as "hello".
# print("Hello") 
# print('Hello') 
# # print multiple line
# """
#  '''Lorem ipsum dolor sit amet,
# consectetur adipiscing elit,
# sed do eiusmod tempor incididunt
# ut labore et dolore magna aliqua.'''
# """
# a = """Lorem ipsum dolor sit amet,
# consectetur adipiscing elit,
# sed do eiusmod tempor incididunt
# ut labore et dolore magna aliqua."""
# print(a) 

# # print value from array
# abc = ("hello world")
# print(abc[0:11]) # 0 is start from h that's mean abc[0] is contain 'h' an 11 is o
# abcd = "Hello, World!"
# print(abcd[-5:-2]) # -5 is print value from back to the front, -5 is o from World! and -2 is l from World!
# print("abcd array contained word total :",len(abcd))
# asd = ("sunat")
# print(asd.replace("sunat","Pok")) # replace the word
# age = 21
# txt = "My name is Pok, and I am {}" # {} is replaced string
# print(txt.format(age))
import numpy as np


print(float('inf'))