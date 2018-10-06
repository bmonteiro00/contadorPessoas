import socket, json


class Gps:

    def __init__(self):
        self.gps_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gps_server.connect(("localhost", "2947"))
        self.gps_server.send('?WATCH={"enable": true,"json":true};')
        self.gps.latitude = None
        self.gps.longitude = None
        self.gps.velocidade = None

    def getlatitude(self):
        return self.gps.latitude

    def getlongitude(self):
        return self.gps.longitude

    def getvelocidade(self):
        return self.gps.speed

    def capturaparametros(self):

        while 1:
            json_response = self.gps_server.recv(2048).strip()
            if json_response.find('"class":"TPV"') != -1:
                json_list = json_response.split(',')
                for pos in json_list:
                    if pos.find("lat") != -1:
                        self.gps.latitude = pos
                    if pos.find("lon") != -1:
                        self.gps.longitude = pos
                    if pos.find("speed") != -1:
                        self.gps.velocidade = pos


        time.sleep(3)

if __name__ == '__main__':
    gps = Gps()
    gps.printparametros()