import matplotlib.pyplot as plt
import csv
import numpy as np

ang_zx = []
ang_zy = []

with open('error_angular_z.csv','r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        ang_zx.append(row[0])
        ang_zy.append(float(row[1]))

lin_zx = []
lin_zy = []

with open('error_linear_z.csv','r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        lin_zx.append(row[0])
        lin_zy.append(float(row[1]))

lin_xx = []
lin_xy = []
with open('error_linear_x.csv','r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        lin_xx.append(row[0])
        lin_xy.append(float(row[1]))


fig, axs = plt.subplots(3)
fig.suptitle('errors (ang_z - lin_z - lin_x)')
axs[0].plot(ang_zx, ang_zy)
axs[1].plot(lin_zx, lin_zy)
axs[2].plot(lin_xx, lin_xy)
"""
plt.plot(x, y)
plt.xlabel('time')
plt.ylabel('error_linear_z')
plt.title('error_linear_z VS time graph', fontsize = 10)
plt.show()
"""
plt.show()
