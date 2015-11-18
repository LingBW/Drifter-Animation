# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:57:34 2015

@author: bling
"""

import numpy as np
import pandas as pd
from matplotlib import animation
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from track_functions import draw_basemap

#filename = 'drift_gomi_2015_1.dat'
#filename = 'drift_wbws_2015_1.dat'
#filename = 'drift_glerl_2015_1.dat'
#filename = 'drift_grnms_2015_2.dat' # not good data
#filename = 'drift_oet_2015_2.dat'
#filename = 'drift_ssnsc_2015_2.dat'
filename = 'drift_ssnsc_2015_1.dat'

print filename
df=pd.read_csv(filename,header=None, delimiter="\s+"); #print df #skiprows=1
#df=pd.read_csv(filename,header=None, delimiter=",",skiprows=1); #print df
colors = ['magenta','cyan','olive','blue','orange','green','red','purple','yellow','black']
# make a datetime
'''dtime=[]
index = np.where(df[0]==int(did))[0]
newData = df.ix[index]#'''
# 1504107010, 1504107011, 1504107014, 1504107015, 150410703, 150410704, 150410706, 150410707, 150410708, 150410709
ids = df[0][:]
idlist = set(ids); #print len(idlist) # 10
save_dir = './Results/'
result = 'banimation'

fig = plt.figure(figsize=(10,9)) #figsize=(16,12)
ax = fig.add_subplot(111)
points = {'lats':[],'lons':[]}  # collect all points we've gained

lons = []; lats = []; loop_num = []; times =[]; ctime = []; toltime = [] #mint = []; maxt = []
basetime = datetime(2015,1,1)
for i in idlist:
    index = np.where(df[0]==i)[0]
    ddata = df.ix[index]; #print len(ddata)
    points['lons'].extend(ddata[7]); points['lats'].extend(ddata[8])
    ts = []; ds = []
    for j in range(len(ddata)):
        #print str(np.array(ddata[2])[j])
        strt = '2015'+'-'+str(np.array(ddata[2])[j])+'-'+str(np.array(ddata[3])[j])+' '+str(np.array(ddata[4])[j])+':'+str(np.array(ddata[5])[j])
        temptime = datetime.strptime(strt,'%Y-%m-%d %H:%M')
        ts.append(temptime) #'''
        ths = (temptime - basetime).total_seconds()/3600
        ds.append(int(round(ths)))
    #mint.append(min(ds)); maxt.append(max(ds))
    times.append(np.array(ts)); ctime.append(np.array(ds)); toltime.extend(ds)
    lons.append(np.array(ddata[7])); lats.append(np.array(ddata[8]))
    loop_num.append(len(ddata[7]))

#mintime = min(mint); maxtime = max(maxt)
#mtime = range(mintime,maxtime+1)
toltime = set(toltime); #print 'Frames number:'
toltime = list(toltime); toltime.sort(); print 'plotting...',len(toltime)

draw_basemap(ax, points)  # points is using here
#print type(lons[0][:])

if result == 'plot':
    for i in range(len(lons)):
        plt.plot(lons[i],lats[i],'-',color = colors[i%10],markersize=20)

#ax.plot(drifter_points['lon'],drifter_points['lat'],'bo-',markersize=6,label='Drifter')
'''ax.annotate(an2,xy=(dr_points['lon'][-1],dr_points['lat'][-1]),xytext=(dr_points['lon'][-1]+0.01*track_days,
            dr_points['lat'][-1]+0.01*track_days),fontsize=6,arrowprops=dict(arrowstyle="fancy"))#'''

if result == 'animation':
    length = 1; 
    if len(toltime)>1000:
        length = 3
    print 'frame:',len(toltime)
    def animate(n): # the function of the animation
        del ax.lines[:]#del ax.collections[:]ax.cla()
        supt = (basetime + timedelta(hours=toltime[n])).strftime('%Y-%m-%d %H:%M')
        plt.suptitle('%s time: %s'%(filename[:-4],supt))               
        for i in range(len(lons)):
            c = colors[i%10]
            if toltime[n] < ctime[i][0]:
                ax.plot(lons[i][0],lats[i][0],'o-',color=c,markersize=6)
            elif toltime[n] > ctime[i][-1]:
                ax.plot(lons[i][-1],lats[i][-1],'o-',color=c,markersize=10)
            #if len(lons[i])>(n+1):        
            #if toltime[n] in ctime[i]:
            #if toltime[n]>=ctime[i][0] and toltime[n]<=ctime[i][-1]:
            else:
                abct = ctime[i] - toltime[n]
                ni = np.argmin(abs(abct)); #print ni
                if ni<5*length :
                    while(ni>=0):
                        ax.plot(lons[i][ni],lats[i][ni],'o-',color=c,markersize=(ni+1))
                        ni=ni-1*length
                else:
                    ax.plot(lons[i][ni],lats[i][ni],'o-',color=c,markersize=10)
                    ax.plot(lons[i][ni-1*length],lats[i][ni-1*length],'o-',color=c,markersize=8)
                    ax.plot(lons[i][ni-2*length],lats[i][ni-2*length],'o-',color=c,markersize=6)
                    ax.plot(lons[i][ni-3*length],lats[i][ni-3*length],'o-',color=c,markersize=4)
                    ax.plot(lons[i][ni-4*length],lats[i][ni-4*length],'o-',color=c,markersize=2)
                    ax.plot(lons[i][ni-5*length],lats[i][ni-5*length],'o-',color=c,markersize=1)
            
    anim = animation.FuncAnimation(fig, animate, frames=len(toltime), interval=50) #
    en_run_time = datetime.now()
    anim.save(save_dir+'%s_%s.gif'%(filename[:-4],en_run_time.strftime("%d-%b-%Y_%H:%M")),writer='imagemagick',dpi=100)

if result == 'banimation':
    seglength = 10; 
    '''if len(toltime)>1000:
        seglength = 3 #'''
    ailoops = int(len(toltime)/seglength)+1
    print 'frame:',ailoops
    def animate(n): # the function of the animation
        del ax.lines[:]#del ax.collections[:]ax.cla()
        n = seglength*n; #print n
        supt = (basetime + timedelta(hours=toltime[n])).strftime('%Y-%m-%d %H:%M')
        plt.suptitle('%s time: %s'%(filename[:-4],supt))               
        
        for i in range(len(lons)): #loop drifters
            
            c = colors[i%10]
            if toltime[n] < ctime[i][0]:
                ax.plot(lons[i][0],lats[i][0],'o-',color=c,markersize=6)
            elif toltime[n] > ctime[i][-1]:
                if toltime[n-seglength]<ctime[i][-1]:
                    lki = ctime[i] - toltime[n-seglength]
                    nik = np.argmin(abs(lki)); #print ni
                    wlp = len(ctime[i])-nik
                    #while (wlp>0):
                    for j in range(wlp):
                        ax.plot(lons[i][-(j+1)],lats[i][-(j+1)],'o-',color=c,markersize=wlp-j+1)
                        #wlp = wlp-1
                    
                else:
                    ax.plot(lons[i][-1],lats[i][-1],'o-',color=c,markersize=10)
            #if len(lons[i])>(n+1):        
            #if toltime[n] in ctime[i]:
            #if toltime[n]>=ctime[i][0] and toltime[n]<=ctime[i][-1]:
            else:
                abct = ctime[i] - toltime[n]
                ni = np.argmin(abs(abct)); #print ni
                
                if ni<seglength:
                    #for k in range(ni):
                    while (ni>=0):
                        ax.plot(lons[i][ni],lats[i][ni],'o-',color=c,markersize=ni+1)
                        ni=ni-1
                else:
                    #segl = seglength
                    #while (segl>0):
                    for k in range(seglength):
                        ax.plot(lons[i][ni-k],lats[i][ni-k],'o-',color=c,markersize=seglength-k)
                        #segl=segl-1
            
    anim = animation.FuncAnimation(fig, animate, frames=ailoops, interval=100) #
    en_run_time = datetime.now()
    # mencoder,imagemagick,ffmpeg
    anim.save(save_dir+'%s_%s.gif'%(filename[:-4],en_run_time.strftime("%d-%b-%Y_%H:%M")),writer='imagemagick',dpi=100)
plt.show()