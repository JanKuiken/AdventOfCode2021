
import numpy as np

depths = np.loadtxt('input.txt')

deeper = depths[1:] > depths[:-1]
cnt = np.sum(deeper)
print(cnt)


windows = depths[:-2] + depths[1:-1] + depths[2:]
deeper = windows[1:] > windows[:-1]
cnt = np.sum(deeper)
print(cnt)


