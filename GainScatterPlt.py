import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numpy import arange,array,ones
from scipy import stats

x = np.array([2.39, 8.4, 14.22, 20.3, 27.0])
y = np.array([2743.5, 1317.7, 516.9, 230.5, 119.8])

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
line = slope*x+intercept

print slope

plt.plot(x, y, 'o', x, line, color='black');
plt.xlabel('Position of Peak (integral value)')
plt.ylabel('Peak Height (from histogram)')
plt.title('Gain Determined from Peak Position and Peak, 68 V')
plt.savefig('GainScatter.pdf')