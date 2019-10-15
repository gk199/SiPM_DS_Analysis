import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as ss
import decimal
from decimal import *

# Edited by: gillian kopp [2019] for SiPM data analysis
# edited from Graham Giovanetti's code read_wav.py 

# load the data from the .txt file
tile_path = '../76K_nolight_69pt5V/' + sys.argv[1] + '.txt'

all_data = []

with open(tile_path) as f:
  for line in f:
      all_data.append(line.strip())
  
  record_len = all_data[0]
  length = record_len.split()
  wf_len = int(length[2])

  file_len = len(all_data)

  # number of records in the input file, +7 to account for headers
  num_rec = file_len/(wf_len + 7)

# modify code from Graham's read_wav
event_n = 0 # list here if events need to be cut out
first_time = 0
last_time = 0
DCR = 0
energy=[]
tile_wfs=[]
trig_wfs=[]
bl_std=[]
trig_times=[]
corr_time=[]
e_moving_avg_hist = []
e_moving_avg_baseline = []

true_time_stamps = []

header_len = 7

noise = []

while event_n < num_rec:
  start = event_n*(wf_len+header_len)
  end = start+(wf_len+header_len)
  record = all_data[start:end]

  #load waveforms
  tile_wf = np.array(record[header_len:header_len+wf_len]).astype(float)
# trig_wf = np.array(record[header_len+wf_len:header_len+2*wf_len]).astype(float)

  #do simple baseline subtraction and energy calculation
  tile_wf = tile_wf - np.sum(tile_wf[0:230])/230.
  noise.extend(tile_wf[0:230]) # this is calculation of noise before filtering the waveform

  # scan integration window to find max for energy calculation
  # this is performing a moving average filtering algorithm
  e_int_max = 0
  window_size = 40
  for i in range(0, wf_len-window_size, 1): # when running use a step size of 1, now doing 10 for speed
    e_int = np.sum(tile_wf[i:i+window_size])/window_size
    if i <=120: # calculate the stdev of the baseline of the filtered wf
      e_moving_avg_baseline.append(e_int)
    if event_n == 0: # make a plot of the first filtered wf for comparison
      e_moving_avg_hist.append(e_int)
    if e_int > e_int_max:
      e_int_max = e_int

  if event_n % 1000 == 0:
  	print 'reached event ' + str(event_n)

  #e_int = np.sum(tile_wf[230:269pt5pt5])/30.
  #energy.append(e_int)
  energy.append(e_int_max)

  #plt.plot(tile_wf)
  #plt.show()
  #print e_int

  #calculate std deviation of pre-trig wf
  bl_std.append(np.std(tile_wf[1:230]))

  #calculate trigger time
# trig_time = np.argmax(np.diff(trig_wf))
# trig_times.append(trig_time)

  #shift trigger and raw wf so that all triggers fall at 490 (avg position)
# tile_wf = np.roll(tile_wf,490-trig_time)

  #save waveforms
  tile_wfs.append(tile_wf)
# trig_wfs.append(trig_wf)

  event_n += 1

  # make sure record length is always the same
  this_wf_len = int(record[0].split()[2])
  assert this_wf_len == wf_len
  # will notify if found a different record length than before


  # save time stamp in a list to make exponential decay for the DCR (time differences as a histogram)
  this_time_stamp = int(record[5].split()[3])

  if event_n == 0:
  	first_time = this_time_stamp
  if event_n == num_rec - 1:
  	last_time = this_time_stamp

  # only want to save time stamps for true PE peaks (not noise) 
  # do this based on the dip between the noise peak and first PE peak
  if e_int_max > 15.7:
  	true_time_stamps.append(this_time_stamp)
  # this is now a list of integers for the absolute time of the photon peaks that were triggered on

#print noise[0:100]
#print noise[1000:1100]
#print len(noise)
print 'noise standard deviation pre-filtered' #stdev for the pre-filtered waveform noise
print np.std(noise)

print 'noise standard deviation filtered wf' # stdev for the filtered waveform
print np.std(e_moving_avg_baseline)
# make a DataFrame
# removed 'trig_wf':trig_wfs, 'trig_time':trig_times  since currently writing for without a trigger
event_df = pd.DataFrame(
  {'tile_wf':tile_wfs,
   'e_int':energy,
   'bl_std':bl_std
  })

#calculate template from 1 PE peak
t_wf = event_df[(event_df['e_int'] > 18.1) & (event_df['e_int'] < 22.3)]['tile_wf'].mean(axis=0)
t_wf2 = event_df[(event_df['e_int'] > 28) & (event_df['e_int'] < 31.5)]['tile_wf'].mean(axis=0)
t_wf3 = event_df[(event_df['e_int'] > 36) & (event_df['e_int'] < 40.7)]['tile_wf'].mean(axis=0)
t_wf4 = event_df[(event_df['e_int'] > 46) & (event_df['e_int'] < 56)]['tile_wf'].mean(axis=0)

print len(t_wf)
# convert x axis from ADC samples to microseconds (*16 is to nanoseconds, /1000 to microseconds)
x_twf = np.r_[0:513*0.016:0.016]

plt.figure(1000)
plt.plot(x_twf, t_wf)
plt.xlabel('Time, microseconds')
plt.ylabel('Amplitude (au)')
plt.title('SiPM Average Waveform 1PE, 76 K, no light, 69.5 V')
#plt.savefig('Data/May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_avgwf_1PE.pdf')
plt.savefig('76K_nolight_69pt5V/76K_nolight_69pt5V_avgwf_1PE.pdf')

plt.figure(2300)
plt.plot(x_twf, t_wf2)
plt.xlabel('Time, microseconds')
plt.ylabel('Amplitude (au)')
plt.title('SiPM Average Waveform 2PE, 76 K, no light, 69.5 V')
#plt.savefig('Data/May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_avgwf_2PE.pdf')
plt.savefig('76K_nolight_69pt5V/76K_nolight_69pt5V_avgwf_2PE.pdf')

plt.figure(3000)
plt.plot(x_twf, t_wf3)
plt.xlabel('Time, microseconds')
plt.ylabel('Amplitude (au)')
plt.title('SiPM Average Waveform 3PE, 76 K, no light, 69.5 V')
#plt.savefig('Data/May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_avgwf_3PE.pdf')
plt.savefig('76K_nolight_69pt5V/76K_nolight_69pt5V_avgwf_3PE.pdf')

plt.figure(4000)
plt.plot(x_twf, t_wf4)
plt.xlabel('Time, microseconds')
plt.ylabel('Amplitude (au)')
plt.title('SiPM Average Waveform 4PE, 76 K, no light, 69.5 V')
#plt.savefig('Data/May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_avgwf_4PE.pdf')


#truncate template (arbitrarily at the moment)
# 1PE average waveform is being used as the template currently
t_wf = t_wf[230:300]

# calculate cross-correlated wfs and add to DataFrame
# there may be a more pythonic way without loop
corr_wfs = []
e_corrs = []

for wf in event_df['tile_wf']:
  c_wf = np.correlate(wf,t_wf)
  corr_wfs.append(c_wf)
  e_corrs.append(np.amax(c_wf))
  corr_time.append(np.argmax(c_wf))
event_df = event_df.assign(corr_wf=corr_wfs)
event_df = event_df.assign(e_corr=e_corrs)
event_df = event_df.assign(corr_time=corr_time)

#print corr_wfs
#print e_corrs

# save DataFrame to hdf5 file
event_df.to_pickle(sys.argv[1]+'.pickle')

#save tempalate waveform
np.save(sys.argv[1]+'.npy',t_wf)

# plt.hist(event_df['trig_time'] - event_df['corr_time'],bins=8000)
# plt.show()

# event_df = event_df[(event_df['e_corr']>-1.195e7)]
# plt.hist2d(event_df['trig_time'] - event_df['corr_time'],event_df['e_corr'],bins=(100,100))
# plt.show()
# event_df.hist(column='e_corr',bins=500)
# plt.show()

plt.figure(100)
plt.plot(true_time_stamps)
plt.xlabel('Event Number')
plt.ylabel('Time Stamps, digitizer clock')
plt.title('SiPM Response, May 2019, 76 K, no light, 69.5 V')
#plt.savefig('Data/May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_timestamp.pdf')
plt.savefig('76K_nolight_69pt5V/76K_nolight_69pt5V_timestamp.pdf')


plt.figure(230)
plt.hist([x for x in np.diff(true_time_stamps) if x>-100],bins=230)
plt.xlim(-5, 8000000)
plt.xlabel('Time Difference')
plt.ylabel('Number of Events')
plt.title('SiPM Response, May 2019, 76 K, no light, 69.5 V')
#plt.savefig('Data/May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_DCR_decay.pdf')

differences = []
true_time_stamps_corr = []
total_time = 0
correction_time = 0
differences = np.diff(true_time_stamps)
# out[n] = a[n+1] - a[n]
for i in range(0,len(true_time_stamps)-1):
	true_time_stamps_corr.append(true_time_stamps[i] + correction_time)
	if differences[i] < -5:
		correction_time = correction_time - differences[i]
		next_zero = true_time_stamps[i+1]

last_time = true_time_stamps_corr[-1]

plt.figure(300)
plt.plot(true_time_stamps_corr)
plt.xlabel('Event Number')
plt.ylabel('Time Stamps, digitizer clock with correction')
plt.title('SiPM Response, May 2019, 76 K, no light, 69.5 V')
#plt.savefig('Data/May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_timestamp_corr.pdf')
plt.savefig('76K_nolight_69pt5V/76K_nolight_69pt5V_timestamp_corr.pdf')

# calculate an exponential fit to the DCR histogram
# use MLE (maximum liklihood estimation method)
# set location to 0 as this is where distribution of events begins
X = np.diff(true_time_stamps_corr)*16*10**(-6)
P = ss.expon.fit(X, floc=0)
print 'exponential fit results (location, scale = 1/DCR in ms = 1/lambda) ' + str(P)
# will return location and scale, with lambda = 1/scale

# now plot the exponential fit
rX = np.linspace(0,230, 1000)
rP = ss.expon.pdf(rX, *P)
# plotted in figure 500, which uses a normalized histogram 

plt.figure(400)
plt.hist(np.diff(true_time_stamps_corr)*16*10**(-6), normed = True, bins=230)
plt.xlim(0, 50)
plt.xlabel('Time Difference (ms)')
plt.ylabel('Number of Events (normalized)')
plt.title('DCR Distribution, 76 K, no light, 69.5 V')
#plt.savefig('Data/May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_DCR_decay.pdf')
plt.savefig('76K_nolight_69pt5V/76K_nolight_69pt5V_DCR_decay.pdf')

plt.figure(500)
plt.hist(np.diff(true_time_stamps_corr)*16*10**(-6), normed=True, bins=230)
plt.xlim(0, 100) #cut out first bin
plt.xlabel('Time Difference (ms)')
plt.ylabel('Number of Events (normalized, log scale)')
plt.plot(rX, rP)
plt.yscale('log')
plt.title('DCR Distribution Log Scale, 76 K, no light, 69.5 V')
#plt.savefig('Data/May2019/76K_nolight_69pt5V/76K_nolight_69pt5V_DCR_decay_expfit.pdf')
plt.savefig('76K_nolight_69pt5V/76K_nolight_69pt5V_DCR_decay_expfit_log.pdf')

# plot of the moving average filtered waveforms
# convert x axis from ADC samples to microseconds (*16 is to nanoseconds, /1000 to microseconds)

x = np.r_[0:473*0.016:0.016]
print len(x)
print len(e_moving_avg_hist)
plt.figure(600)
plt.plot(x,e_moving_avg_hist)
plt.xlabel('Time, microseconds')
plt.ylabel('Amplitude (au, charge)')
plt.title('SiPM Waveform from Moving Average Filtering, 76 K, no light, 69.5 V')
plt.savefig('76K_nolight_69pt5V/76K_nolight_69pt5V_filteredwf.pdf')

print 'number of events ' + str(num_rec)
print 'time difference total ' + str(last_time)
DCR = float(num_rec) / float(last_time)
print 'DCR ' + str(DCR) 

#plt.show()

