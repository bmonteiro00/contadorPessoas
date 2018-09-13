#
# Maintainer:   Cambus
# Version:      0.0.1
#
#

import os
import time
import platform
import logging
from uuid import getnode as get_mac
from Contador_v1 import Contador

class CamBus:

    def __init__(self):
        self.frame = None
        
        # Dados básicos: sistema operacional, PID, e o MAC (para gerar um nome único no MQTT)
        self.OS = platform.system()
        self.myPID = os.getpid()
        self.myID = hex(get_mac())
        self.myMode = os.getenv('MODE')
        
        # Sistema de log: pega da variavel de ambiente LOGLEVEL
            #logger.debug('debug message')
            #logger.info('info message')
            #logger.warn('warn message')
            #logger.error('error message')
            #logger.critical('critical message')
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        if os.getenv('LOGLEVEL') == 'ERROR':
            logger.setLevel(logging.ERROR)        
        elif os.getenv('LOGLEVEL') == 'DEBUG':
            logger.setLevel(logging.DEBUG)        
        else:
            logger.setLevel(logging.INFO)      

        # create a file handler
        handler = logging.FileHandler('CamBus.log')
        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)

        # Conexão MQTT
        self.mq = os.getenv('MQTT')
        
        if self.mq == "AWS":
            logging.info('using AWS')
            
        elif self.mq == "ECLIPSE":
            print("using (iot.eclipse.org)")
            
        else:
            self.mq = "fake"
            print("using default (fake stub)")
        
#        if self.os == 'Linux':
 #           call('clear', shell = True)
  #      elif self.os == 'Windows':
   #         call('cls', shell = True) */
   
        logger.info('CabBus successfully started')


    def runCamBus(self):
        print('logLevel= ' +str(logging.getLogger().getEffectiveLevel()) )
        logging.info('OS=   ' +self.OS)
        logging.info('PID=  ' +str(self.myPID) ) 
        logging.info('ID=   ' +self.myID)
        logging.info('mq=   ' +self.mq)
        logging.info('mode= ' +str(self.myMode) )
        
        if( self.myMode ):
            Contador().detectPeople()
        else:
            print('please use export MODE=x to enable Counting Process')
        
 

if __name__ == '__main__':
    CamBus().runCamBus()
    