import random

uagent_list = ['Android'] * 46 + ['iOS'] * 42 + ['Symbian'] * 3 + ['Java ME'] * 3 + ['Windows'] * 2 + ['Java ME'] * 1 + ['BlackBerry'] * 1 + ['Kindle'] * 1 + ['Other'] * 1

a =random.choice(uagent_list)
print(a)