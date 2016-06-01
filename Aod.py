class AOD:
    AODCount = 0

    def __init__(self, latitude, longitude, aod_12, aod_030, nprofiles, uprofiles, month, year):
        self.latitude = latitude
        self.longitude = longitude
        self.aod_12 = aod_12
        self.aod_030 = aod_030
        self.nprofiles = nprofiles
        self.uprofiles = uprofiles
        self.month = month
        self.year = year
        AOD.AODCount += 1

    def displayCount(self):
        print "Total AOD %d" % AOD.AODCount

    def displayAOD(self):
        print "month :", self.month, "year :", self.year, "Latitude : ", self.latitude, ", Longitude: ", self.longitude, ", aod12 ", self.aod_12, ", nprofiles ", self.nprofiles, ", uprofiles ", self.uprofiles

    def getLat(self):
        print self.latitude

    def getYear(self):
        print self.year

    def getMonth(self):
        print self.month

    def getAod(self):
        return self.aod_12
