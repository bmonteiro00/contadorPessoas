#
# Maintainer:   Cambus
# Version:      0.0.1
#
#

import paho.mqtt.client as paho
import socket
import ssl
from time import sleep
from random import uniform
import sys

# Error values
MQTT_HOST_EMPTY = -31
MQTT_PORT_EMPTY = -32


class CamMQttClient:
    def __del__(self):
        print ('MQtt client[] died')

    def __init__(self, pLogger, pOS):
        self._frame = None
        self._logger = pLogger
        self._OS = pOS
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
    
    def connect(self):
    
        if self._fakeFlag == True:
            return
            
        if (not self._host) or (self._host == ""):
            self._logger.critical('[Host] cannot be empty! Use .setup() first')
            sys.exit(MQTT_HOST_EMPTY)
            
        elif (not self._port) or (self._host == ""):
            self._logger.critical('[Port] cannot be empty! Use .setup() first')
            sys.exit(MQTT_PORT_EMPTY)
        
        self._mq.connect(self._host, int(self._port), keepalive=60)
        
        ####self._mq.publish("sptrans/teste", "TEssssssteee", qos=0)
        self._mq.loop_forever()

    
    def AWSConnect(self):
        clientId = "Teste"
        thingName = "Teste"
        caPath = "aws-iot-rootCA.pem"
        certPath = "e866e9eb47-certificate.pem.crt.txt"
        keyPath = "e866e9eb47-private.pem.key"

        self._mq.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    
    def onConnect(self, client, userdata, flags, rc):
        global _connFlag
        self._connFlag = True

        if rc==0:
            self._logger.info('MQTT connected to [' +self._host +':' +self._port +']')
        else:
            self._logger.error('MQTT error [' +rc +' when connecting to [' +self._host +':' +self._port +']')
            pass #todo 
            # 0: Connection successful 1: Connection refused - incorrect protocol version 2: Connection refused - invalid client identifier 3: Connection refused - server unavailable 4: Connection refused - bad username or password 5: Connection refused
        
        client.subscribe('sptrans/#')

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


