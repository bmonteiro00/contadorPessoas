#
# Maintainer:   Cambus
# Version:      0.0.1
#
#

import os
import time
from contextlib import suppress
import sys 
#kkkimport RPi.GPIO as GPIO

class CamSensors:

    def __del__(self):
        if hasattr(self, 'GPIO'):
            self.GPIO.cleanup()
            
        print ('Sensor[] died')

    def __init__(self, pLogger, pOS):
        self.frame = None
       
        self.logger = pLogger
        self.OS = pOS
        
        # Tenta importar a biblioteca GPIO correta para o hardware
        try:
            if self.OS == 'Windows':
                # Fake GPIO
                #self.GPIO = '{ fake}' 
                pass
                
            elif self.OS == 'rasp':     # para a Raspberry PI
                import RPi.GPIO as GPIO
                
            elif self.OS == 'dragon?':  # Para a Dragon
                from GPIOLibrary import GPIOProcessor

                self.GPIO = GPIOProcessor()

            else:
                # Do the default
                self.logger.critical('Unknown operational system [' +self.OS +']')
                raise
            
        except RuntimeError:
            self.logger.critical('Error importing GPIO for system [%s]!  This is probably because you need superuser privileges.  You can achieve this by using [sudo] to run your script', self.OS)
            sys.exit(-10)
            
        # sucesso
        self.logger.info('Sensors[%s] successfully loaded', self.OS)   

    def getSensorValues(self):
        
        print('logLevel= ' +str(logging.getLogger().getEffectiveLevel()) )
        logging.info('OS=   ' +self.OS)
 

if __name__ == '__main__':
    CamSensors().getSensorValues()
    