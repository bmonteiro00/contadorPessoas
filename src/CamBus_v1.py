#
# Maintainer:   Cambus
# Version:      0.0.1
#
#

import os
import time
import datetime
import platform
import logging
import configparser
from contextlib import suppress

from uuid import getnode as get_mac
from Contador_v1 import Contador
from Sensors_v1  import CamSensors

configFilename = "CamBus.ini"

class CamBus:

    def __del__(self):
        self.saveConfig()
        print ('CamBus[', self.myPID, '] died')

    def __init__(self):
        self.frame = None
        
        ########################################################################################
        # Dados básicos: sistema operacional, PID, e o MAC (para gerar um nome único no MQTT)
        self.OS = platform.system()
        self.myPID = os.getpid()
        self.myID = hex(get_mac())
        self.myMode = os.getenv('MODE')
        
        self.setLogger()
        self.readConfig()
        
        self.mySensor = CamSensors(self.logger, self.OS)        
        self.logger.info('CamBus successfully started')    

    def setLogger(self):
        ########################################################################################
        # Sistema de log: pega da variavel de ambiente LOGLEVEL
            #logger.debug('debug message')
            #logger.info('info message')
            #logger.warn('warn message')
            #logger.error('error message')
            #logger.critical('critical message')
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        if os.getenv('LOGLEVEL') == 'ERROR':
            self.logger.setLevel(logging.ERROR)        
        elif os.getenv('LOGLEVEL') == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)        
        else:
            self.logger.setLevel(logging.INFO)      

        # create a file handler
        handler = logging.FileHandler('CamBus.log')
        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(handler)

    ########################################################################################
    # Salva parâmetros atuais        
    def saveConfig(self):
        # Update timestamp
        ts = str(time.time() )
        agora = str(datetime.datetime.now())        
        
        #with suppress(Exception):
        cfgFile = open(configFilename, 'w')            
        ###self.config = configparser.ConfigParser()
        self.busConfig.set('DEFAULT', 'LAST_TIMESTAMP', ts)
        self.busConfig.set('DEFAULT', 'LAST_SHUTDOWN',  agora)
            
        self.busConfig.set('MQTT', 'mqtt', self.mq)
            
        self.busConfig.write(cfgFile)
        cfgFile.close()
        
    ########################################################################################
    # Lê dados de configuração e último timestamp válido
    def readConfig(self):
        self.busConfig = configparser.ConfigParser()
        self.busConfig.read(configFilename)
        cfgfile = open(configFilename, 'r')
        
        # valores default
        with suppress(Exception):
            self.busConfig.add_section('MQTT')
            self.busConfig.add_section('BUS')
            self.busConfig.add_section('SENSORS')

        self.busConfig.set('BUS', 'name', 'Vila Cruzeiro')
        self.busConfig.set('BUS', 'car', '11234')
        self.busConfig.set('BUS', 'line', '6422-10')
        self.busConfig.set('BUS', 'status', 'moving')
        self.busConfig.set('SENSORS', 'timestamp',  '2018-09-15 09:16:57.977719')
        self.busConfig.set('SENSORS', 'people_in',  '20')
        self.busConfig.set('SENSORS', 'people_out', '22')
        self.busConfig.set('SENSORS', 'temp',       '24.1')
        self.busConfig.set('SENSORS', 'co2',        '99.9')
        self.busConfig.set('SENSORS', 'pressure',   '99.9')
        self.busConfig.set('SENSORS', 'gps',        '20.34')
        self.busConfig.set('SENSORS', 'rain',        'true')
        self.busConfig.set('SENSORS', 'weight',        '12t')
        
        self.lastTimestamp = '???'
        with suppress(Exception):
            self.lastTimestamp = self.busConfig['DEFAULT']['LAST_TIMESTAMP'] 
        
        agora = str(datetime.datetime.now())
        logging.info('Starting now: [%s]', agora)
        logging.info('Last shutdown was: [%s]', self.lastTimestamp)
        
        # List all contents
        '''
        print("List all contents")
        for section in config.sections():
            print("Section: %s" % section)
            for options in config.options(section):
                print("x %s:::%s:::%s" % (options,
                                          config.get(section, options),
                                          str(type(options))))
        '''   
        
        ########################################################################################
        # Conexão MQTT
        ###kkkself.mq = os.getenv('MQTT')
        self.mq = 'fake'
        
        if self.mq == "AWS":
            logging.info('using AWS')            
        elif self.mq == "ECLIPSE":
            print("using (iot.eclipse.org)")            
        elif self.mq == "FAKE":
            self.mq = "fake"
        else:
            with suppress(Exception):
                self.mq = self.busConfig['MQTT']['MQ'] 
            
        
#        if self.os == 'Linux':
 #           call('clear', shell = True)
  #      elif self.os == 'Windows':
   #         call('cls', shell = True) */
   
    def connectMQTT(self):
        print('falta fazer!')


    def runCamBus(self):
        print('logLevel= ' +str(logging.getLogger().getEffectiveLevel()) )
        logging.info('OS=   ' +self.OS)
        logging.info('PID=  ' +str(self.myPID) ) 
        logging.info('ID=   ' +self.myID)
        logging.info('mq=   ' +self.mq)
        logging.info('mode= ' +str(self.myMode) )
        
        self.connectMQTT()
        
        if( self.myMode ):
            Contador().detectPeople()
        else:
            print('please use export MODE=x to enable Counting Process')
        
 

if __name__ == '__main__':
    CamBus().runCamBus()
    