#
# Maintainer:   Cambus
# Version:      0.0.1
#
#

import paho.mqtt.client as paho
import socket
import ssl
import sys
from time import sleep
from random import uniform
import json

# Error values
MQTT_HOST_EMPTY = -31
MQTT_PORT_EMPTY = -32
MQTT_CONNECT_ERR = -33


class CamMQttClient:
    def __del__(self):
        print ('MQtt client[] died')

    def __init__(self, logger, OS, lastTimestamp):
        self._frame = None
        self._logger = logger
        self._OS = OS
        self._lastTimestamp = lastTimestamp
        self._connFlag = False
        self._host = ''
        self._port = ''
        self._fakeFlag = False
        
        self._mq = paho.Client()
        self._mq.on_connect = self.onConnect
        self._mq.on_message = self.onMessage
        self._mq.on_disconnect = self.onDisconnect

        #mq.on_log = on_log

    def setupFake(self):
        self._fakeFlag = True
    
    def setup(self, host, port):
        self._host = host
        self._port = port
        
    def publish(self, topic, json_string):
        print('publish(' +self._host +')  ' +topic +', ' +json_string)
        self._mq.publish(topic, json_string, qos=0)
    
    def connect(self, topic, subscribe_to, json_string):
    
        if self._fakeFlag == True:
            return
            
        if (not self._host) or (self._host == ""):
            self._logger.critical('[Host] cannot be empty! Use .setup() first')
            sys.exit(MQTT_HOST_EMPTY)
            
        elif (not self._port) or (self._host == ""):
            self._logger.critical('[Port] cannot be empty! Use .setup() first')
            sys.exit(MQTT_PORT_EMPTY)
        
        try:
            self._mq.connect(self._host, int(self._port), keepalive=60)
        except (IOError, RuntimeError):
            self._logger.critical('MQTT failed to connect to [' +self._host +':' +self._port +']')
            sys.exit(MQTT_CONNECT_ERR)
        
        self._logger.debug('self._mq.publish(' +topic +', ' +json_string +', qos=0)')
        self._mq.subscribe(subscribe_to)
        self._mq.publish(topic, json_string, qos=0)
        #self._mq.loop_forever()

    
    def AWSConnect(self, caPath, certPath, keyPath, topic, subscribeTo, jsonString):
        self._mq.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.connect(topic, subscribeTo, jsonString)
    
    def onConnect(self, client, userdata, flags, rc):
        global _connFlag
        self._connFlag = True

        print('entrei!')
        if rc==0:
            self._logger.info('MQTT connected to [' +self._host +':' +self._port +']')
        else:
            self._logger.error('MQTT error [' +rc +' when connecting to [' +self._host +':' +self._port +']')
            pass #todo 
            # 0: Connection successful 1: Connection refused - incorrect protocol version 2: Connection refused - invalid client identifier 3: Connection refused - server unavailable 4: Connection refused - bad username or password 5: Connection refused
        
        client.subscribe('/aws/action/#')
        print('saí daqui!')

    def onMessage(self, client, userdata, msg):
        print(msg.topic +' [' +str(msg.payload) +']')
        
    def onDisconnect(self, client, userdata, rc):
        if rc != 0:
            self._logger.info('MQTT was disconnected from [' +self._host +':' +self._port +'] with error [' +str(rc) +']')
            # ToDo: reconectar????

        else:
            self._logger.error('MQTT connection was forcibly closed by the remote host [' +rc +']')
    
    #def on_log(client, userdata, level, buf):
    #    print(msg.topic+" "+str(msg.payload))


