import numpy as np
import matplotlib.pyplot as plt
import time

# import file from another folder
import sys
sys.path.append('../')
from adder import digit_add
from subtractor import digit_sub
from combine import digit_combine

time_add = digit_add()
time_sub = digit_sub()
time_combine = digit_combine()

print(time_add)
print(time_sub)
print(time_combine)

# data to plot
fp = open("tmp.txt", "r")
n_groups = 3
cor = np.zeros((3,3), dtype=float)
for i in range(3):
    for j in range(3):
        cor[i][j] = fp.readline()
fp.close()

# create plot
index = np.arange(n_groups)
bar_width = 0.2
opacity = 0.8
 
rects1 = plt.bar(index - bar_width, cor[0], bar_width,
alpha=opacity,
color='b',
label='adder')
 
rects2 = plt.bar(index, cor[1], bar_width,
alpha=opacity,
color='g',
label='subtractor')

rects3 = plt.bar(index + bar_width, cor[2], bar_width,
alpha=opacity,
color='r',
label='combine')

plt.ylabel('Correctness(%)')
plt.xticks(index, ('3-digit', '4-digit', '5-digit'))
plt.legend()

plt.savefig('../img/digit.png')
plt.show()
os.remove("tmp.txt")
