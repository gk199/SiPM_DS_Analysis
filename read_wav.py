import sys
import numpy as np
import pandas as pd
import pysndfile
import matplotlib.pyplot as plt
# (fig_width, fig_height) = plt.rcParams['figure.figsize']
# fig_size = [fig_width * 2, fig_height * 2]

# load the data from the .wav file
file_path = 'data/nuvhd_lf_1x_tile15_77K_65V_5VoV_' + sys.argv[1] + '.wav'
file_len = pysndfile.sndio.get_info(file_path, extended_info=True)[3]
data = pysndfile.sndio.read(file_path, dtype=np.int16)

header_len = data[0][1]
n_chan = data[0][10]
wf_len = data[0][6]
rec_len = header_len + wf_len * n_chan
num_rec = file_len/rec_len

event_n = 0
energy=[]
tile_wfs=[]
trig_wfs=[]
bl_std=[]
trig_times=[]
corr_time=[]

while event_n < num_rec:
  start = event_n*rec_len
  end = start+rec_len
  record = data[0][start:end]

  #load waveforms
  tile_wf = np.array(record[header_len:header_len+wf_len]).astype(float)
  trig_wf = np.array(record[header_len+wf_len:header_len+2*wf_len]).astype(float)

  #do simple baseline subtraction and energy calculation
  tile_wf = tile_wf - np.sum(tile_wf[1:7001])/7000.
  e_int = np.sum(tile_wf[8900:12000])/-3100.
  energy.append(e_int)

  #calculate std deviation of pre-trig wf
  bl_std.append(np.std(tile_wf[1:7000]))

  #calculate trigger time
  trig_time = np.argmin(np.diff(trig_wf))
  trig_times.append(trig_time)

  #shift trigger and raw wf so that all triggers fall at 8968 (avg position)
  tile_wf = np.roll(tile_wf,8968-trig_time)

  #save waveforms
  tile_wfs.append(tile_wf)
  trig_wfs.append(trig_wf)

  event_n += 1

# make a DataFrame
event_df = pd.DataFrame(
  {'trig_wf':trig_wfs,
   'tile_wf':tile_wfs,
   'e_int':energy,
   'bl_std':bl_std,
   'trig_time':trig_times
  })

#calculate template from 1 PE peak
t_wf = event_df[(event_df['e_int'] > 3.5) & (event_df['e_int'] < 5.5)]['tile_wf'].mean(axis=0)
#truncate template (arbitrarily at the moment)
t_wf = t_wf[8800:12000]

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

# save DataFrame to hdf5 file
event_df.to_pickle(sys.argv[1]+'.pickle')

#save tempalate waveform
np.save(sys.argv[1]+'.npy',t_wf)

plt.hist(event_df['trig_time'] - event_df['corr_time'],bins=8000)
plt.show()

event_df = event_df[(event_df['e_corr']>-1.195e7)]
plt.hist2d(event_df['trig_time'] - event_df['corr_time'],event_df['e_corr'],bins=(100,100))
plt.show()
event_df.hist(column='e_corr',bins=500)
plt.show()
