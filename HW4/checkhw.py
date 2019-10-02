# question 1
eval("""16384""") 
# question 2 number only or char
eval("""7""") 
# question 3
eval("""{
        'H': ['a', 'c', 'h', 'i'],
        'I': ['a', 'h'],
        'J': ['h', 'i'],
        'K': ['a', 'c', 'h', 'i'],
        'M': ['i'],
        'S': ['a', 'c', 'h', 'i'],
        'T': ['a', 'c', 'i']
    }"""
) 
# Question 4 check first bracket
eval("""{'M': 'i'}""")
# Question 4 check second bracket
eval("""
    {
        'H': ['i'],
        'I': ['a'],
        'J': ['h'],
        'K': ['a'],
        'M': ['i'],
        'S': ['a'],
        'T': ['a','c','i']
    }
  """)

# Question 4 check by first bracket
eval("""{'VAR1': 'VAL1'}""")
# then second bracket

eval("""{
    'VAR1': ['VAL1', 'VAL2'],
    'VAR2': ['VAL2', 'VAL4'],
    'VAR3': ['VAL4'],
    'VAR4': ['VAL1', 'VAL2', 'VAL4'],
    'VAR5': ['VAL2', 'VAL4'],
    'VAR6': ['VAL2', 'VAL4'],
    'VAR7': ['VAL2']
}""")
