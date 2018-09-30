#
# Maintainer:   Cambus
# Version:      0.0.1
#
#

import os
import time
import datetime
from contextlib import suppress
import sys 
#kkkimport RPi.GPIO as GPIO

# Error values
SENSOR_CANNOT_IMPORT_GPIO = -21


class CamSensors:
    def __del__(self):
        if hasattr(self, 'GPIO'):
            self.GPIO.cleanup()
            
        print ('Sensor[] died')

    def __init__(self, logger, OS):
        self.frame = None
       
        self._logger = logger
        self._OS = OS
        
        # Tenta importar a biblioteca GPIO correta para o hardware
        try:
            if self._OS == 'Windows':
                # Fake GPIO
                #self.GPIO = '{ fake}' 
                pass
                
            elif self._OS == 'rasp':     # para a Raspberry PI
                import RPi.GPIO as GPIO
                
            elif self._OS == 'dragon?':  # Para a Dragon
                from GPIOLibrary import GPIOProcessor

                self.GPIO = GPIOProcessor()

            else:
                # Do the default
                self._logger.critical('Unknown operational system [' +self._OS +']')
                raise
            
        except RuntimeError:
            self._logger.critical('Error importing GPIO for system [%s]!  This is probably because you need superuser privileges.  You can achieve this by using [sudo] to run your script', self.OS)
            sys.exit(SENSOR_CANNOT_IMPORT_GPIO)
        
         # Default value 
        self._Temp = 23
        # sucesso
        self._logger.info('Sensors[%s] successfully loaded', self._OS)   

    def getJson(self):
        if self._OS == 'Windows':
            self._Temp += 1
            self._logger.info('getSensorValues(' +self._OS +')')
            Data =  [
                        {
                            'name': 'Temperatura',
                            'type': 'centigrade',
                            'value':  self._Temp
                        } , 
                        {
                            'name': 'CO2',
                            'type': 'ppm',
                            'value': self._Temp
                        }
                    ]
         
        #Data['GPS'] = 'bla'
        return Data

 
 
if __name__ == '__main__':
    CamSensors().getSensorValues()
     