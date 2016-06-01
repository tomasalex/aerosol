from mpl_toolkits.basemap import Basemap#, cm
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
# import scipy as sp
from scipy.misc import imread
import pylab


def perMonth(a, b):
    plt.plot(b, a)
    plt.grid()


def mapPerPeriod(aodperDegree, lats, longs, title, savefile, cmapname,minv=0,maxv=0):
    # Make plot with vertical (default) colorbar
  
    fig, ax = plt.subplots()

    data = aodperDegree
    datafile = cbook.get_sample_data('C:/Users/alex/marspython/aerosol/gr.png')
    img = imread(datafile)

    ax.imshow(img, zorder=1, alpha=0.3,
              extent=[float(min(longs))-0.5, float(max(longs))+0.5, float(min(lats)) - 0.5, float(max(lats))+0.5])

    if minv<>0 or maxv<>0 :
        cax = ax.imshow(data, zorder=0, interpolation='spline16', cmap=cm.get_cmap(cmapname),
                    extent=[float(min(longs)), float(max(longs)), float(min(lats)), float(max(lats))],
                    vmin=minv,vmax=maxv)
    else:
        cax = ax.imshow(data, zorder=0, interpolation='spline16', cmap=cm.get_cmap(cmapname),
                    extent=[float(min(longs)), float(max(longs)), float(min(lats)), float(max(lats))])
    ax.set_title(title)

    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    #cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
    cbar = fig.colorbar(cax)
    #cbar.ax.set_yticklabels(['< -1', '0', '> 1'])  # vertically oriented colorbar
    pylab.savefig(savefile + ".png")


    #plt.show()

def plot_data(data,lon_data, lat_data, periodname, AODcatname,maptype,cmapname,minv=0,maxv=0,folder=""):
    fig = plt.figure()
    #ax = fig.add_axes([0.1,0.1,0.8,0.8])

    m = Basemap(llcrnrlon=19,llcrnrlat=34,urcrnrlon=29,urcrnrlat=42,
                resolution='h',projection='cass',lon_0=24,lat_0=38)

    nx = int((m.xmax-m.xmin)/1000.)+1
    ny = int((m.ymax-m.ymin)/1000.)+1
    topodat = m.transform_scalar(data,lon_data,lat_data,nx,ny)
    
    if minv<>0 or maxv<>0 :
        im = m.imshow(topodat,cmap=plt.get_cmap(cmapname),vmin=minv,vmax=maxv)
    else:
        im = m.imshow(topodat,cmap=plt.get_cmap(cmapname))
 

    m.drawcoastlines()
    m.drawmapboundary()
    m.drawcountries()
    m.drawparallels(np.arange(35,42.,1.), labels=[1,0,0,1])
    m.drawmeridians(np.arange(-20.,29.,1.), labels=[1,0,0,1])
    cb = m.colorbar(im,"right", size="5%", pad='2%')
    title=maptype+" AOD "+AODcatname+" "+periodname+" 2007-2014"
    plt.title(title)
    pylab.savefig(folder+maptype+"AOD"+AODcatname+"_"+periodname + ".png")
    #plt.show()

def plot_regline(data, lat, lon, slope, intercept,months, period, periodlabel, AODrange, plotAOD=False, aodvalues=[],folder=""):
    fig = plt.figure(figsize=(8,7))
    
    ax1=fig.add_subplot(111)
    
    mlist=[]
    for m in months:
        if int(m.split('-')[0]) in period:
            mlist.append(m.split('-')[1]+m.split('-')[0])
    mlist.sort()
    axlabels=mlist[:]
    for ms in axlabels:
        i=axlabels.index(ms)
        if i%3==0 or len(axlabels)<30:
            axlabels[i]=ms[4:]+'-'+ms[:4]
        else: 
            axlabels[i]=''

    x = np.arange(0,len(data))
    
    ax1.scatter(x, data[x],color='blue', label='AOD deseasonalized')
    plt.xticks(x, axlabels, rotation=45)
    
    x_plot = np.linspace(0,len(data),100*len(data))
    ax1.plot(x_plot, x_plot*slope + intercept, label='Regression Line')
    
    if plotAOD:
        aodvals=np.zeros(len(mlist))
        for e in aodvalues:
            if e.month in period and lat==e.latitude and lon==e.longitude:
                k=mlist.index(str(e.year)+str(e.month).zfill(2))
                aodvals[k]=float(e.aod_12)
            
        ax2 = fig.add_subplot(111, sharex=ax1, frameon=False)
        ax2.scatter(x, aodvals[x],color='green',label='AOD values')
        #ax2.scatter(x, data[x]/100.0,color='red')
  
        ax2.yaxis.tick_right()
        for t in ax2.get_xticklabels():
            t.set_visible(False)
        #ax2.yaxis.set_label_position("right")
        #ylabel("Right Y-Axis Data")

    ax1.legend(loc='upper left')
    ax2.legend()
    plt.title('Regression line at '+lat+' '+lon+'. Slope : '+"{0:.2f}".format(slope)+" "+periodlabel+" "+AODrange)
    pylab.savefig(folder+"reglineat_"+lat+"_"+lon+"_"+periodlabel+"_"+AODrange+".png")

  