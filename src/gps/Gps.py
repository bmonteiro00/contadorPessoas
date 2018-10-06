import socket, json


class Gps:

    def __init__(self):
        self.gps_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gps_server.connect(("localhost", 2947))
        self.gps_server.send('?WATCH={"enable": true,"json":true};')
        self.latitude = None
        self.longitude = None
        self.velocidade = None

    def getlatitude(self):
        return self.latitude

    def getlongitude(self):
        return self.longitude

    def getvelocidade(self):
        return self.velocidade

    def capturaparametros(self):

        while 1:
            json_response = self.gps_server.recv(2048).strip()
            if json_response.find('"class":"TPV"') != -1:
                json_list = json_response.split(',')
                for pos in json_list:
                    if pos.find("lat") != -1:
                        self.latitude = pos
                    if pos.find("lon") != -1:
                        self.longitude = pos
                    if pos.find("speed") != -1:
                        self.velocidade = pos


        time.sleep(3)

if __name__ == '__main__':
    gps = Gps()
    gps.capturaparametros()
    gps.getlatitude()
    gps.getlongitude()
    gps.getvelocidade()