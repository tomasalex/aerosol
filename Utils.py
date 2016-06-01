import os
import Aod
import datetime
import numpy as np
import math
from statistics import mean,stdev
from scipy.stats import linregress
# from main import aodvalues, monthYears
#from scipy.ndimage.measurements import variance

def load_data(aodcol):
    dir = "./CALIPSO_data/Total_AOD/"
    
    files = os.listdir(dir)
    files.sort()
    monthYears = []
    aodvalues = []
    AodToDouble = []
    for file in files:
        if file.endswith(".txt"):
            with open(dir + file) as f:
                data = f.read()
                # parse filename and take month and year
                p = file.split('-')
                monthYears.append(p[0].split('_')[3] + '-' + p[1].split('.')[0])
                data = data.split('\n')
                for i in range(1, len(data) - 1):
                    linesplit = data[i].split('\t')
    
                    rows = linesplit[0]
                    cols = rows.split(' ')
                    Latitude = cols[0]
                    Longitude = cols[1]
                    AOD_12 = cols[aodcol]
                    AOD_030 = cols[2]
                    Number_of_profiles = cols[6]
                    Utilized_profiles = cols[7]
                    month = int(p[0].split('_')[3])
                    year = int(p[1].split('.')[0])
                    aod_element = Aod.AOD(Latitude, Longitude, AOD_12, AOD_030, Number_of_profiles, Utilized_profiles, month, year)
                    # aod_element.displayAOD()
                    aodvalues.append(aod_element)
                    # tom_index = next(index for (index, d) in enumerate(aodvalues) if d["name"] == "Tom")
    return aodvalues, monthYears

def aodPerMonthGraph(aodvalues):
    AodToDouble = []
    plotVal = []
    xdates = []
    for j in range(2007, 2014):
        k = 0
        n = 0
        for i in range(1, 12):
            for element in aodvalues:
                if element.getYear() == j and element.getMonth() == i and float(element.getAod()) >= 0:
                    k += float(element.getAod())
                    n += 1
                    # print element.displayAOD()
            AodToDouble.append(str(i) + "_" + str(j) + "_" + str(float(k / n)))
            plotVal.append(float(k / n))
            xdates.append(datetime.datetime(j, i, 5))
    return plotVal, xdates, AodToDouble


def aodDeseasonalisation(aodvalues, AodToDouble):
    plotVal = []
    xdates = []

    for j in range(2007, 2014):
        k = 0
        n = 0
        for i in range(1, 12):
            content = [x for x in AodToDouble if x.startswith(str(i) + '_' + str(j))]
            for element in aodvalues:
                if element.getYear() == j and element.getMonth() == i and float(element.getAod()) >= 0:
                    k += float(element.getAod())
                    n += 1
                    # print element.displayAOD()
            monthMean = content[0].split('_')[2]
            plotVal.append(float(k / n) - float(monthMean))
            xdates.append(datetime.datetime(j, i, 5))
    return plotVal, xdates


    # l = filter(lambda x: str(i) + '_' + str(j) in x, AodToDouble)
    # ll = [s for s in AodToDouble if str(i) + '_' + str(j) in s]
    # lll = any(item.startswith(str(i) + '_' + str(j)) for item in AodToDouble)
    # [s for s in AodToDouble if str(i) + '_' + str(j) in s]

def getStat(aodvalues):
    aods=[]
    aodpercent=[]
    nan=0
    zerovals=0
    for e in aodvalues:
        if isfloat(e.aod_12):
            aods.append(float(e.aod_12))
            if float(e.aod_12)==0:
                zerovals+=1
            if float(e.aod_030)>0 :
                aodpercent.append(float(e.aod_12)/float(e.aod_030))
        if e.aod_12=='NaN':
            nan+=1
    m=mean(aods)
    s=stdev(aods)
    mp=mean(aodpercent)
    sp=stdev(aodpercent)
     
    return m,s,mp,sp,nan,zerovals
    


def getLats(aodvalues):
    allLats = []
    for el in aodvalues:
        if el.latitude not in allLats:
            allLats.append(el.latitude)

    allLongs = []
    for el in aodvalues:
        if el.longitude not in allLongs:
            allLongs.append(el.longitude)

    return allLats, allLongs


def GetPeriodData(period, aodvalues, allLats, allLongs):
    data = np.ndarray((len(allLats), len(allLongs)))
    i = -1
    for lati in allLats:
        i += 1
        j = -1
        for longi in allLongs:
            j += 1
            AODSum = 0
            aodcounter = 0
            for e in aodvalues:
                if e.latitude == lati and e.longitude == longi and e.month in period and float(e.aod_12) > 0:
                    aodcounter += 1
                    AODSum += float(e.aod_12)
            if aodcounter > 0:
                data[i][j] = AODSum / aodcounter
    return data

def isfloat(value):
  try:
    float(value)
    if not math.isnan(float(value)):
        return True
  except ValueError:
    return False

def GetPeriodData_v2(period, aodvalues, allLats, allLongs, rejectzeros=True, uprof=0):
    data = np.zeros((len(allLats), len(allLongs)))
    counters = np.zeros((len(allLats), len(allLongs)))
    countzeros = np.zeros((len(allLats), len(allLongs)))


    for e in aodvalues:
        i=allLats.index(e.latitude)
        j=allLongs.index(e.longitude)
        if not rejectzeros :
            numcheck=isfloat(e.aod_12)
            if float(e.aod_12)<0.000000000000000001 :
                countzeros[i][j]+=1
        else :
            numcheck=False
            if isfloat(e.aod_12):
                if float(e.aod_12)>0.0 :
                    numcheck=True
                    
        if e.uprofiles.isdigit():
            uprofcheck=(int(e.uprofiles)>=uprof)
        else :
            uprofcheck=False
        
        if e.month in period and numcheck and uprofcheck :
            data[i][j]+=float(e.aod_12)
            counters[i][j] += 1
            
        #elif not isfloat(e.aod_12):
        #    print 'NAN value ',e.aod_12,' for ', e.month,' ',e.year, ' at ', allLats[i], allLongs[j]
        
        #if float(e.aod_12)>0.1:
        #    print 'Big value ',e.aod_12,' for ', e.month,' ',e.year, ' at ', allLats[i], allLongs[j]
 
    for ind, x in np.ndenumerate(data) :
        if data[ind[0]][ind[1]]<0.00000000000000001 :
            print 'zero aod for period ', period, ' at ', allLats[ind[0]], allLongs[ind[1]]
            
            
        if counters[ind[0]][ind[1]]>0 :
            data[ind[0]][ind[1]] /= counters[ind[0]][ind[1]]
        else :
            print 'Only NAN values for period ', period, ' at ', allLats[ind[0]], allLongs[ind[1]]
        
        #if countzeros[ind[0]][ind[1]]>0 :
        #    print 'num of zero values for period ', period, ' at ', allLats[ind[0]], allLongs[ind[1]], ' : ', countzeros[ind[0]][ind[1]]
 
    return data



def GetDeseasonalizedData(period, aodvalues, allLats, allLongs, months, meanAOD, rejectzeros=True, uprof=0):
    
    mlist=[]
    for m in months:
        if int(m.split('-')[0]) in period:
            mlist.append(m.split('-')[1]+m.split('-')[0])
    mlist.sort()
    
    data = np.zeros((len(allLats), len(allLongs), len(mlist)))
    
    slopedata = np.zeros((len(allLats), len(allLongs)))
    interceptdata = np.zeros((len(allLats), len(allLongs)))
    
    for e in aodvalues:
        i=allLats.index(e.latitude)
        j=allLongs.index(e.longitude)
        if not rejectzeros :
            numcheck=isfloat(e.aod_12)
        else :
            numcheck=False
            if isfloat(e.aod_12):
                if float(e.aod_12)>0.0 :
                    numcheck=True
        
        if e.month in period and numcheck and int(e.uprofiles)>=uprof:
            k=mlist.index(str(e.year)+str(e.month).zfill(2))
            if meanAOD[i][j]>0 :
                data[i][j][k]=(float(e.aod_12)-meanAOD[i][j])/meanAOD[i][j]*100
        
    x = np.arange(0,len(mlist))
    for ind, e in np.ndenumerate(data[:,:,-1]) :
        slope, intercept, r_value, p_value, std_err = linregress(x,data[ind[0]][ind[1]])
        slopedata[ind[0]][ind[1]]=slope
        interceptdata[ind[0]][ind[1]]=intercept
  
    return slopedata, interceptdata, data 


