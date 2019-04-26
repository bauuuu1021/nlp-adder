import numpy as np
import matplotlib.pyplot as plt
import time
import os

# import file from another folder
import sys
sys.path.append('../')
from adder import origin_add
from subtractor import origin_sub
from combine import origin_combine

def executeT(f):
    start = time.time()
    f()
    return time.time()-start

exT = np.zeros((3), dtype=float)
exT[0] = executeT(origin_add)
exT[1] = executeT(origin_sub)
exT[2] = executeT(origin_combine)

# load correctness
cor = np.zeros((3), dtype=float)
fp = open("tmp.txt", "r")
for i in range(3):
    cor[i] = float(fp.readline())
fp.close()

# plot
label = ['adder', 'subtractor', 'combine']
pos = np.arange(len(label))
plt.bar(pos, cor, label = 'correctness (%)', align = "center", width = 0.3)
plt.xticks(pos, label)
plt.legend()    

for i, v in enumerate(cor):
    plt.text(pos[i] - 0.08, v + 0.1, str(v))

plt.savefig('../img/origin.png')
plt.show()

print(exT)
os.remove("tmp.txt")