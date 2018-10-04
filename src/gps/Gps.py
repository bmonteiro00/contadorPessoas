import gps, os, time


class Gps:

    def __init__(self):
        self.gps = gps.gps()
        print('Satellites (total of', len(session.satellites), ' in view)')
        for i in session.satellites:
            print('\t', i)

    def getlatitude(self):
        return self.gps.fix.latitude

    def getlongitude(self):
        return self.gps.fix.longitude

    def getaltitude(self):
        return self.gps.fix.altitude

    def getvelocidade(self):
        return self.gps.speed

    def printparametros(self):
        while 1:
            # a = altitude, d = date/time, m=mode,
            # o=postion/fix, s=status, y=satellites

            print
            print(' GPS reading')
            print('----------------------------------------')
            print('latitude    ', self.gps.fix.latitude)
            print ('longitude   ', self.gps.fix.longitude)
            print ('time utc    ', self.gps.utc, session.fix.time)
            print ('altitude    ', self.gps.fix.altitude)
            #print 'eph         ', self.gps.fix.eph
            print ('epv         ', self.gps.fix.epv)
            print ('ept         ', self.gps.fix.ept)
            print ('speed       ', self.gps.fix.speed)
            print ('climb       ', self.gps.fix.climb)

        time.sleep(3)

if __name__ == '__main__':
    gps = Gps()
    gps.printparametros()