import sys
import glob
from scipy import stats
import numpy as np
import pandas as pd
#import pysndfile
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from sklearn import mixture
import matplotlib.mlab

# Edited by: gillian kopp [2019] for SiPM data analysis
# edited from Graham Giovanetti's code

from pylab import rcParams
rcParams['figure.figsize'] = 9.6, 7.2

(fig_width, fig_height) = plt.rcParams['figure.figsize']
fig_size = [fig_width * 2, fig_height * 2]

# load a single data file
event_df = pd.read_pickle(sys.argv[1])

# load all of the data files
# file_list = glob.glob('processed/*.pickle')
# df_list = []
#
# for file in file_list:
#   df_list.append(pd.read_pickle(file))
#
# event_df = pd.concat(df_list, ignore_index=True)

# cut pedestal events
# event_df = event_df[(event_df['e_corr']>130000)]
# cut all events that aren't early
# event_df = event_df[((event_df['corr_time']-8800)>100)]

# event_df.to_pickle('100ns_late_events.pickle')

#mean,std=norm.fit(event_df['e_int'])

clf = mixture.GaussianMixture(n_components=3, covariance_type='full')
clf.fit((event_df['e_int'].to_numpy()).reshape(-1, 1)) #turn into a numpy array instead
m1, m2, m3 = clf.means_ # mean
w1, w2, w3 = clf.weights_ # height
c1, c2, c3 = clf.covariances_ # width
#histdist = matplotlib.pyplot.hist(event_df['e_int'], 4000, normed=True)
#plotgauss1 = lambda x: plt.plot(x,w1*matplotlib.mlab.normpdf(x,m1,np.sqrt(c1))[0], linewidth=3)
#plotgauss2 = lambda x: plt.plot(x,w2*matplotlib.mlab.normpdf(x,m2,np.sqrt(c2))[0], linewidth=3)
#plotgauss3 = lambda x: plt.plot(x,w3*matplotlib.mlab.normpdf(x,m3,np.sqrt(c3))[0], linewidth=3)
#plotgauss1(histdist[1])
#plotgauss2(histdist[1])
#plotgauss3(histdist[1])

print 'made gaussians with means ', m1, m2, m3
print 'made gaussians with weights ', w1, w2, w3
print 'made gaussians with stdev ', c1, c2, c3
# energy histogram
#plt.hist(event_df['e_corr']/1e6,bins=1000)
plt.figure(1000)
plt.hist(event_df['e_int'],bins=4000)
x = np.linspace(0,45,4000)
p1 = stats.norm.pdf(x,m1,c1)*w1
p2 = stats.norm.pdf(x,m2,c2)*w2
p3 = stats.norm.pdf(x,m3,c3)*w3
print len(x)
print len(p1.reshape(-1,1))
plt.plot(x,p1.reshape(-1,1),'k',linewidth=2)
plt.plot(x,p2.reshape(-1,1),'k',linewidth=2)
plt.plot(x,p3.reshape(-1,1),'k',linewidth=2)
plt.xlabel('Charge (arb units)')
plt.xlim(0, 45)
plt.ylabel('Counts')
plt.title('Energy Spectrum from Moving Average Filtering, 68 V Bias')
plt.savefig('Energy Spectrum.pdf')
plt.show()



#(mu,sigma) = norm.fit(event_df['e_int'])

# energy histogram from convolution
plt.figure(2000)
plt.hist(event_df['e_corr'],bins=4000)
plt.xlabel('Energy (arb units)')
plt.xlim(-5, 20000)
plt.ylabel('Counts')
plt.title('Energy Spectrum from Convolution, 68 V Bias')
plt.savefig('Energy Spectrum Convolution.pdf')
#plt.show()

# # 2d event time vs energy histogram
#plt.hist2d(event_df['corr_time']-8800,event_df['e_corr']/1e6,bins=(500,200), range=np.array([(-1000,1000),(0,2)]), norm=LogNorm())
plt.hist2d(event_df['corr_time'],event_df['e_corr'],bins=(500,200), range=np.array([(-1000,1000),(0,2)]))
plt.xlabel('event time (ns)')
plt.ylabel('energy (arb)')
plt.colorbar()
plt.savefig('Energy vs Event Time.pdf')

# plt.show()

# cut pedestal events
# event_df = event_df[(event_df['e_corr']>130000)]
# event_df = event_df[(event_df['e_corr']<210000)]

# keep only pedestal events
event_df = event_df[(event_df['e_corr']<130000)]

# e_range = []
# for i in range(1000,11000,10000):
# # for i in range(8550,9050,50):
#   e_range.append([i,i+50])

# event_df.corr_wf = np.roll(event_df.corr_wf, 8800-event_df.corr_time)

for index,row in event_df.iterrows():
  event_df.set_value(index,'corr_wf',np.roll(row['corr_wf'],8800-row['corr_time']))
  event_df.set_value(index,'tile_wf',np.roll(row['tile_wf'],8800-row['corr_time']))
corr_wf = event_df['corr_wf'].mean(axis=0)
wf = event_df['tile_wf'].mean(axis=0)
#print wf
# np.save('noise_avg_wf.npy',wf)
# plt.subplot(2,1,1)
# plt.plot(corr_wf[8000:10000],'b',label='cc wf')
# plt.legend(loc='upper right')
# plt.subplot(2,1,2)
# plt.plot(wf[8000:10000],color='purple',label='raw wf')
# plt.legend(loc='upper right')
# plt.xlabel('ns')
# plt.show()

# avg_wfs = []
# for range in e_range:
#   temp = event_df[(event_df['corr_time']>range[0]) & (event_df['corr_time']<range[1])]
#   # temp.corr_wf = np.roll(temp.corr_wf,event_df.corr_time)
#   wf = temp['corr_wf'].mean(axis=0)
#   avg_wfs.append(wf)
#   plt.plot(wf,label=('%i to %i' % ((range[0]-8800),(range[1]-8800))))
# avg_wfs = np.array(avg_wfs)
#
# plt.show()

# event_df.corr_wf = np.roll(event_df.corr_wf, 5000+(-1*event_df.corr_time))
# wf = event_df['corr_wf'].mean(axis=0)
#
#
# for index,row in event_df.iterrows():
#   plt.plot(row['corr_wf'],alpha=0.1,color='gray')
# plt.plot(wf,'r')
# plt.show()

# e_range = []
# for i in range(1000,5000,50):
# for i in range(8550,9050,50):
#   e_range.append([i,i+50])
#
# avg_wfs = []
#
# for range in e_range:
#   temp = event_df[(event_df['corr_time']>range[0]) & (event_df['corr_time']<range[1])]
#   print range, temp.shape
#   wf = temp['tile_wf'].mean(axis=0)
#   avg_wfs.append(wf)
#   plt.plot(wf,label=('%i to %i' % ((range[0]-8800),(range[1]-8800))))
# avg_wfs = np.array(avg_wfs)
# np.save('avg_corr_wfs_timebins',avg_wfs)
#
# plt.legend(loc='upper right')
# plt.show()
# event time cmoparison histogram
# plt.hist(event_df['corr_time']-8800,bins=100, range =np.array([-1000,1000]),color='red',label="0.13 < E < 0.33")
# plt.hist(event_df2['corr_time']-8800,bins=100, range =np.array([-1000,1000]),color='blue', alpha=0.5,label="0.13 < E < 0.21")
# # plt.yscale('log')
# plt.xlabel('event time (ns)')
# plt.ylabel('counts')
# plt.title('tile 15')
# plt.legend(loc="upper right")
# plt.show()
# event_df = event_df[(event_df['e_corr']>-1.195e7)]
# plt.hist2d(event_df['trig_ `time'] - event_df['corr_time'],event_df['e_corr'],bins=(100,100))
# plt.show()
# event_df.hist(column='e_corr',bins=500)
# plt.show()
