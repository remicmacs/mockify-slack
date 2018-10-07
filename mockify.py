import random

def tossCoin(): return random.random() <= 0.5

def randCase(c): return c.upper() if tossCoin() else c.lower()

def mockify(s): return ''.join([randCase(el) for el in s])
