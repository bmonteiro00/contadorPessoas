#
# Maintainer:   Cambus
# Version:      0.0.1
#
#

import os
import sys
import time
import datetime
import threading
import platform
import logging
import configparser
from contextlib import suppress
import json

from uuid import getnode as get_mac
from Contador_v1    import Contador
from Sensors_v1     import CamSensors
from MqttClient_v1  import CamMQttClient

configFilename = "CamBus.ini"

# Error values
CAMBUS_INVALID_MQ_TYPE = -32

class CamBus:

    def __del__(self):
        self.saveConfig()
        print ('CamBus[', self._PID, '] died')

    def __init__(self):
        self.frame = None
        
        ########################################################################################
        # Dados básicos: sistema operacional, PID, e o MAC (para gerar um nome único no MQTT)
        self._OS = platform.system()
        self._PID = os.getpid()
        self._ID = hex(get_mac())
        
        self.setLogger()
        self.readConfig()
        
        self._sensor = CamSensors(self._logger, self._OS)
        self._counter = Contador(self._logger)
        self._mqtt = CamMQttClient(self._logger, self._OS, self._lastTimestamp)
        self._subscribeTo = self._busConfig['MQTT']['SUBSCRIBE_TO']
        self._topic =       self._busConfig['MQTT']['BASE_TOPIC'] +self._name +'/' + self._car
        self._logger.info('CamBus successfully started')    

    def setLogger(self):
        ########################################################################################
        # Sistema de log: pega da variavel de ambiente LOGLEVEL
            #self._logger.debug('debug message')
            #self._logger.info('info message')
            #self._logger.warn('warn message')
            #self._logger.error('error message')
            #self._logger.critical('critical message')

        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger(__name__)
        
        if os.getenv('LOGLEVEL') == 'ERROR':
            self._logger.setLevel(logging.ERROR)        
        elif os.getenv('LOGLEVEL') == 'DEBUG':
            self._logger.setLevel(logging.DEBUG)        
        else:
            self._logger.setLevel(logging.INFO)      

        # create a file handler
        handler = logging.FileHandler('CamBus.log')
        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # add the handlers to the logger
        self._logger.addHandler(handler)

    ########################################################################################
    # Salva parâmetros atuais        
    def saveConfig(self):
        # Update timestamp
        ts = str(time.time() )
        agora = str(datetime.datetime.now())        
        
        #with suppress(Exception):
        cfgFile = open(configFilename, 'w')            
        ###self.config = configparser.ConfigParser()
        self._busConfig.set('DEFAULT', 'LAST_TIMESTAMP', ts)
        self._busConfig.set('DEFAULT', 'LAST_SHUTDOWN',  agora)
            
        self._busConfig.set('MQTT', 'mq',   self._mq)
        self._busConfig.set('MQTT', 'host', self._host)
        self._busConfig.set('MQTT', 'port', self._port)
        
        self._busConfig.write(cfgFile)
        cfgFile.close()
        
    ########################################################################################
    # Lê dados de configuração e último timestamp válido
    def readConfig(self):
        self._busConfig = configparser.ConfigParser()
        self._busConfig.read(configFilename)
        cfgfile = open(configFilename, 'r')
        
        # Sessões default
        with suppress(Exception):
            self._busConfig.add_section('MQTT')
            self._busConfig.add_section('MQTT_eclipse')
            self._busConfig.add_section('MQTT_local')
            self._busConfig.add_section('MQTT_aws')
            self._busConfig.add_section('BUS')
            self._busConfig.add_section('SENSORS')

        self._busConfig.set('DEFAULT', 'Contador', 'Contador_v1')
        self._busConfig.set('DEFAULT', 'Sensors', 'Sensors_v1')
        
        # valores default
        self._busConfig.set('MQTT', 'mq', 'aws')
        self._busConfig.set('MQTT', 'host', 'a3k400xgjmh5lk.iot.us-east-2.amazonaws.com')
        self._busConfig.set('MQTT', 'port', '8883')
        self._busConfig.set('MQTT', 'base_topic', '/aws/')
        self._busConfig.set('MQTT', 'subscribe_to', '/aws/command/#')
        
        self._busConfig.set('MQTT', 'clientId', 'Teste')
        self._busConfig.set('MQTT', 'thingName', 'Teste')
        self._busConfig.set('MQTT', 'caPath', 'aws-iot-rootCA.pem')
        self._busConfig.set('MQTT', 'certPath', 'e866e9eb47-certificate.pem.crt.txt')
        self._busConfig.set('MQTT', 'keyPath', 'e866e9eb47-private.pem.key')

        
        self._busConfig.set('MQTT_eclipse', 'mq', 'eclipse')
        self._busConfig.set('MQTT_eclipse', 'host', 'm2m.eclipse.org')
        self._busConfig.set('MQTT_eclipse', 'port', '1883')
        
        self._busConfig.set('MQTT_local', 'mq', 'mqtt')
        self._busConfig.set('MQTT_local', 'host', 'localhost')
        self._busConfig.set('MQTT_local', 'port', '1883')
        
        self._busConfig.set('MQTT_aws', 'mq', 'aws')
        self._busConfig.set('MQTT_aws', 'host', 'a3k400xgjmh5lk.iot.us-east-2.amazonaws.com')
        self._busConfig.set('MQTT_aws', 'port', '8883')
        
        self._busConfig.set('BUS', 'name', 'Vila Cruzeiro')
        self._busConfig.set('BUS', 'car', '11234')
        self._busConfig.set('BUS', 'line', '6422-10')
        self._busConfig.set('BUS', 'status', 'moving')
        self._busConfig.set('SENSORS', 'timestamp',  '2018-09-15 09:16:57.977719')
        self._busConfig.set('SENSORS', 'people_in',  '20')
        self._busConfig.set('SENSORS', 'people_out', '22')
        self._busConfig.set('SENSORS', 'temp',       '24.1')
        self._busConfig.set('SENSORS', 'co2',        '99.9')
        self._busConfig.set('SENSORS', 'pressure',   '99.9')
        self._busConfig.set('SENSORS', 'gps',        '20.34')
        self._busConfig.set('SENSORS', 'rain',       'true')
        self._busConfig.set('SENSORS', 'weight',     '12t')
        self._busConfig.set('SENSORS', 'publish_interval', '5')
        
       
        #Cria valores default falsos
        self._lastTimestamp = '???'
        
        with suppress(Exception):
            self._lastTimestamp = self._busConfig['DEFAULT']['LAST_TIMESTAMP'] 
        
            self._name =  self._busConfig['BUS']['name']
            self._car  =  self._busConfig['BUS']['car']
            self._line =  self._busConfig['BUS']['line']

            self._mq =       self._busConfig['MQTT']['mq'] 
            self._host =     self._busConfig['MQTT']['host'] 
            self._port =     self._busConfig['MQTT']['port'] 
            self._caPath =   self._busConfig['MQTT']['caPath']
            self._certPath = self._busConfig['MQTT']['certPath']
            self._keyPath =  self._busConfig['MQTT']['keyPath']
            
        self._publishInterval = int(self._busConfig['MQTT']['publish_interval'] )

        agora = str(datetime.datetime.now())
        self._logger.info('Starting now: [%s]', agora)
        self._logger.info('Last shutdown was: [%s]', self._lastTimestamp)
        
        
        
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
        
           
        
#        if self.os == 'Linux':
 #           call('clear', shell = True)
  #      elif self.os == 'Windows':
   #         call('cls', shell = True) */
   
    def getBusJson(self):
        Data = {
                'Name': self._name,
                'Car':  self._car,
                'Line': self._line,
                'Status': 'start up',
                'Last_timestamp': self._lastTimestamp,
                'PID': self._PID
            }
        #Data['Name'] = 'nommeee'
        return Data
        
    def connectMQTT(self):
        json_string = json.dumps(self.getBusJson())
       
        
        if  self._mq == 'fake':
            self._mqtt.setupFake()

        elif self._mq == 'mqtt'  or  self._busConfig['MQTT']['MQ'] == 'eclipse':
            self._mqtt.setup(self._host, self._port)
            self._mqtt.connect(self._topic, self._subscribeTo, json_string)
            
        elif self._mq == 'eclipse':
            self._mqtt.setup(self._host, self._port)
            self._mqtt.connect(self.topic, self._subscribeTo, json_string)
            
        elif self._mq == 'aws':
            self._mqtt.setup(self._host, self._port)
            self._mqtt.AWSConnect(self._caPath, self._certPath,  self._keyPath, self._topic, self._subscribeTo, json_string )

        else:
            self._logger.critical('[MQ] = ' +self._mq +', is an invalid option!')
            sys.exit(CAMBUS_INVALID_MQ_TYPE)

    def runCamBus(self):
        print('logLevel= ' +str(logging.getLogger().getEffectiveLevel()) )
        self._logger.info('OS=   ' +self._OS)
        self._logger.info('PID=  ' +str(self._PID) ) 
        self._logger.info('ID=   ' +self._ID)
        self._logger.info('mq=   ' +self._mq)
        self._logger.info('threadId= ' +str(threading.current_thread()) )
        
        self.connectMQTT()
        
        self._counter.run()
        
        
        while True:
            # Loop principal do programa
            time.sleep( self._publishInterval )
            bData = {
                    'BUS': True,
                    'COUNTER': True,
                    'SENSORS': True                    
                }
            test='{"str": 11, "dex": 12, "con": 10, "int": 16, "wis": 14, "cha": 13} '
            
            bData['SENSORS'] = self._sensor.getJson()
            bData['BUS'] =     self.getBusJson()
            bData['BUS']['Status'] = 'running'
            
            bData['COUNTER'] = self._counter.getJson()
            #test['dex']='blá blá'
            # {"error_1395946244342":"valueA","error_1395952003":"valueB"}
            #print(self._sensor.getSensorValues())
            #self._mqtt.publish(self._topic, json.dumps(test))
            #self._mqtt.publish(self._topic, json.dumps(self._sensor.getSensorValues()) )
            self._mqtt.publish(self._topic, json.dumps(bData) )
        
        if(self._countFlag):
            Contador().detectPeople()
        else:
            print('please use export COUNT=x to enable Counting Process')
        
       

if __name__ == '__main__':
    CamBus().runCamBus()
    