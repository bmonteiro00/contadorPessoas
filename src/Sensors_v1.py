#
# Maintainer:   Cambus
# Version:      0.0.1
#
#

import os
import time
import platform
import datetime
import logging
#from contextlib import suppress
import sys 
#kkkimport RPi.GPIO as GPIO

# Error values
SENSOR_CANNOT_IMPORT_GPIO = -21
SENSOR_UNKNOWN_SO = -22

class CamSensors:
    def __del__(self):
        if hasattr(self, 'GPIO'):
            self.GPIO.cleanup()
            
        print ('Sensor[] died')

    def __init__(self, logger, so):
        self.frame = None
       
        self.LOG = logger
        self._OS = so
        
        # Tenta importar a biblioteca GPIO correta para o hardware
        try:
            if (self._OS == 'Windows') or (self._OS == 'vmlinux') :
                # Fake GPIO
                #self.GPIO = '{ fake}' 
                pass
                
            elif self._OS == 'raspberrypi':     # para a Raspberry PI
                import RPi.GPIO as GPIO
                
            elif self._OS == 'dragon?':  # Para a Dragon
                from GPIOLibrary import GPIOProcessor

                self.GPIO = GPIOProcessor()

            else:
                # Do the default
                self.LOG.critical('Unknown operational system [' +self._OS +']')
                sys.exit(SENSOR_UNKNOWN_SO)
            
        except RuntimeError:
            self.LOG.critical('Error importing GPIO for system [%s]!  This is probably because you need superuser privileges.  You can achieve this by using [sudo] to run your script', self.OS)
            sys.exit(SENSOR_CANNOT_IMPORT_GPIO)
        
         # Default value 
        self._Temp = 23
        # sucesso
        self.LOG.info('Sensors[%s] successfully loaded', self._OS)

    # Return CPU temperature as a character string                               
    def getRaspCPUTemperature(self):
        res = os.popen('vcgencmd measure_temp').readline()
        return (res.replace("temp=","").replace("'C\n",""))


    def getJson(self):
        self.LOG.debug('getSensorValues(' +self._OS +')')
        
        if self._OS == 'Windows':
            self._Temp += 1

            Data =  [
                        {
                            'name': 'Temp',
                            'type': 'centigrade',
                            'value':  self._Temp
                        } , 
                        {
                            'name': 'CO2',
                            'type': 'ppm',
                            'value': self._Temp
                        }
                    ]
                    
        elif self._OS == 'raspberrypi':
            Data = [
                    {
                        'name': 'Temp',
                        'type': 'centigrade',
                        'value':  self.getRaspCPUTemperature()
                    } , 
                    {
                        'name': 'CO2',
                        'type': 'ppm',
                        'value': self._Temp
                    }
                ]
        else:
            # Do the default
            self.LOG.critical('Unknown operational system [' +self._OS +']')
            sys.exit(SENSOR_UNKNOWN_SO)
         
        #Data['GPS'] = 'bla'
        return Data

 
 
if __name__ == '__main__':
    LOG = logging.getLogger(__name__)
    handler = logging.FileHandler('CamBus.log')
    LOG.addHandler(handler)
    
    print(platform.system())
    #try:
    CamSensors(LOG).getSensorValues()
    #except:
    #    pass
     