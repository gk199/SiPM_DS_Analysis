import numpy as np
import matplotlib.pyplot as plt

#with open('PlotData_March27_124K.txt') as f:
#    lines = f.readlines()
#    x = [int(line.split('\t')[0]) for line in lines]
#    y = [int(line.split('\t')[1]) for line in lines]
#PlotData_March27_124K.close()

a = []

with open('May2019/76K_nolight_68V/wave4.txt') as f:
	for line in f:
		a.append(line.strip())

# waveforms in ADC samples
a1 = a[7:520]
a2 = a[7+520*1:520+520*1]
a3 = a[7+520*2:520+520*2]
a4 = a[7+520*3:520+520*3]
a5 = a[7+520*4:520+520*4]
a6 = a[7+520*5:520+520*5]

# convert the wf ADC sample to micro seconds now
#A1 = [int(i) * 16/1000 for i in a1]
#A2 = [int(i) * 16/1000 for i in a2]
#A3 = [int(i) * 16/1000 for i in a3]
#A4 = [int(i) * 16/1000 for i in a4]
#A5 = [int(i) * 16/1000 for i in a5]
#A6 = [int(i) * 16/1000 for i in a6]

# convert x axis from ADC samples to microseconds (*16 is to nanoseconds, /1000 to microseconds)
x = np.r_[0:513*0.016:0.016]

plt.figure(100)
plt.plot(x, a1)
plt.xlabel('Time, microseconds')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, 76 K, no light, 68 V')
plt.savefig('May2019/SeptFix/76K_nolight_68V/76K_nolight_68V_raw1.pdf')

plt.figure(200)
plt.plot(x, a2)
plt.xlabel('Time, microseconds')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, 76 K, no light, 68 V')
plt.savefig('May2019/SeptFix/76K_nolight_68V/76K_nolight_68V_raw2.pdf')

plt.figure(300)
plt.plot(x, a3)
plt.xlabel('Time, microseconds')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, 76 K, no light, 68 V')
plt.savefig('May2019/SeptFix/76K_nolight_68V/76K_nolight_68V_raw3.pdf')

plt.figure(400)
plt.plot(x, a4)
plt.xlabel('Time, microseconds')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, 76 K, no light, 68 V')
plt.savefig('May2019/SeptFix/76K_nolight_68V/76K_nolight_68V_raw4.pdf')

plt.figure(500)
plt.plot(x, a5)
plt.xlabel('Time, microseconds')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, 76 K, no light, 68 V')
plt.savefig('May2019/SeptFix/76K_nolight_68V/76K_nolight_68V_raw5.pdf')

plt.figure(600)
plt.plot(x, a6)
plt.xlabel('Time, microseconds')
plt.ylabel('SiPM Response')
plt.title('SiPM Response, 76 K, no light, 68 V')
plt.savefig('May2019/SeptFix/76K_nolight_68V/76K_nolight_68V_raw6.pdf')

#plt.figure(680)
#plt.plot(a)
#plt.xlabel('Time')
#plt.ylabel('SiPM Response')
#plt.title('SiPM Response, April 30, square wave test')

plt.show()

f.close()
