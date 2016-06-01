import os
import Aod
import Utils
import plots
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import datetime

print('Hello :)')
print(os.path.dirname(os.path.abspath(__file__)))

plt.close('all')


AOD12=4
AOD01=3
AOD030=2
AODranges=[AOD030,AOD01,AOD12]
#AODranges=[AOD12]

for AODcol in AODranges:
    AODrange_labels=['0-30km','0-1km','1-2km']
    AODcat=AODranges.index(AODcol)
    
    aodvalues, monthYears  = Utils.load_data(AODranges[AODcat])
    
    mn,stdv, mpn, stdvp,nan,zerovals =Utils.getStat(aodvalues)
    
    print('Sample mean:', mn,'Sample std dev:', stdv)
    print('Sample mean of AOD percentage of AOD 0-30:', mpn,'Sample std dev of AOD percentage of AOD 0-30:', stdvp)
    print('Number of NaN values:', nan,'Number of zero values:', zerovals)
    
    #exit()
    
    allLats, allLongs = Utils.getLats(aodvalues)
    allLats_s=allLats[:]
    allLats.sort(reverse=True)
    winter = [12, 1, 2]
    spring = [3, 4, 5]
    summer = [6, 7, 8]
    autumn = [9, 10, 11]
    year = list(range(1, 13))
    
    #periods=[winter, spring, summer, autumn, year ]
    periods=[winter, spring, summer, autumn, year]
    #periods=[winter]
    #periods=[year]
    
    period_names=['Winter', 'Spring', 'Summer', 'Autumn', 'Year' ]
    #period_names=['Year' ]
    
    
    for period in periods:
        pnum=periods.index(period)
        meanAODperDegree = Utils.GetPeriodData_v2(period, aodvalues, allLats, allLongs,False,uprof=15)
        slopeAODperDegree, intercAODdegree, alldeseasondata=Utils.GetDeseasonalizedData(period, aodvalues, allLats, allLongs, monthYears, 
                                                      meanAODperDegree, False, uprof=15)
        
    #     plots.plot_regline(alldeseasondata[5][5], allLats[5], allLongs[5], slopeAODperDegree[5][5], intercAODdegree[5][5], 
    #                        monthYears, period,period_names[pnum],AODrange_labels[AODcat],True, aodvalues)
        
    #     plots.plot_data(np.flipud(meanAODperDegree), np.asarray(map(float,allLongs)),np.asarray(map(float, allLats_s)), 
    #                          period_names[pnum],AODrange_labels[AODcat],"Mean",'jet',minv=0,maxv=0.10,folder="./graphsfix/")
          
    #     plots.plot_data(np.flipud(slopeAODperDegree), np.asarray(map(float,allLongs)),np.asarray(map(float, allLats_s)), 
    #                          period_names[pnum],AODrange_labels[AODcat],"Slope",'gnuplot',minv=-7,maxv=7,folder="./graphsfix/")
    
        plots.plot_regline(alldeseasondata[5][5], allLats[5], allLongs[5], slopeAODperDegree[5][5], intercAODdegree[5][5], 
                           monthYears, period,period_names[pnum],AODrange_labels[AODcat],True, aodvalues,folder="./graphsprof15/")
        
        plots.plot_data(np.flipud(meanAODperDegree), np.asarray(map(float,allLongs)),np.asarray(map(float, allLats_s)), 
                             period_names[pnum],AODrange_labels[AODcat],"Mean",'jet',folder="./graphsprof15/")
        plots.plot_data(np.flipud(slopeAODperDegree), np.asarray(map(float,allLongs)),np.asarray(map(float, allLats_s)), 
                             period_names[pnum],AODrange_labels[AODcat],"Slope",'gnuplot',folder="./graphsprof15/")



plt.show()

# plt.figure(2)
# x, y, AodToDouble = Utils.aodPerMonthGraph(aodvalues)
# plots.perMonth(x, y)
#
# plt.figure(3)
# x, y = Utils.aodDeseasonalisation(aodvalues, AodToDouble)
# plots.perMonth(x, y)
# plt.show()
