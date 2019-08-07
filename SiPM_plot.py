import numpy as np
import matplotlib.pyplot as plt

#with open('PlotData_March27_124K.txt') as f:
#    lines = f.readlines()
#    x = [int(line.split('\t')[0]) for line in lines]
#    y = [int(line.split('\t')[1]) for line in lines]
#PlotData_March27_124K.close()

a = []

with open('May2019/76K_nolight_69pt5V/wave4.txt') as f:
	for line in f:
		a.append(line.strip())

a1 = a[7:520]
a2 = a[7+520*1:520+520*1]
a3 = a[7+520*2:520+520*2]
a4 = a[7+520*3:520+520*3]
a5 = a[7+520*4:520+520*4]
a6 = a[7+520*5:520+520*5]


plt.figure(100)
plt.plot(a1)
plt.xlabel('Time')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, May 2019, 76 K, no light, 69.5 V')
plt.savefig('May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_raw1.pdf')

plt.figure(200)
plt.plot(a2)
plt.xlabel('Time')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, May 2019, 76 K, no light, 69.5 V')
plt.savefig('May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_raw2.pdf')

plt.figure(300)
plt.plot(a3)
plt.xlabel('Time')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, May 2019, 76 K, no light, 69.5 V')
plt.savefig('May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_raw3.pdf')

plt.figure(400)
plt.plot(a4)
plt.xlabel('Time')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, May 2019, 76 K, no light, 69.5 V')
plt.savefig('May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_raw4.pdf')

plt.figure(500)
plt.plot(a5)
plt.xlabel('Time')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, May 2019, 76 K, no light, 69.5 V')
plt.savefig('May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_raw5.pdf')

plt.figure(600)
plt.plot(a6)
plt.xlabel('Time')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, May 2019, 79 K, no light, 69.5 V')
plt.savefig('May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_raw6.pdf')

#plt.figure(69pt50)
#plt.plot(a)
#plt.xlabel('Time')
#plt.ylabel('SiPM Response')
#plt.title('SiPM Response, April 30, square wave test')

plt.show()

f.close()
