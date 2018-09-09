#
# Maintainer:   Cambus
# Version:      0.0.1
#
#

import numpy as np
import cv2
import Pessoa
import time


class Contador:

    def __init__(self):
        self.frame = None

    def detectPeople(self):

        #Contadore de entrada e saída
        cnt_up = 0
        cnt_down = 0

        #Fonte de video
        #cap = cv2.VideoCapture(0) # Descomente para usar a camera.
        #cap = cv2.VideoCapture("C:\\Users\\Bruno\\Documents\\GitHub\\Contador\\peopleCounter.avi") #Captura um video
        #cap = cv2.VideoCapture("C:\\Users\\Bruno\\Documents\\GitHub\\Contador\\d.mp4") #Captura um video
        cap = cv2.VideoCapture("C:\\Users\\Bruno\\Documents\\GitHub\\Contador\\bus.avi") #Captura um video

        #Descomente para imprimir as propriedades do video
        """for i in range(19):
            print (i, cap.get(i))"""

        #Metodo GET para pegar width e height do frame
        w = cap.get(3)
        h = cap.get(4)

        x_meio = int(w/2)
        y_meio = int(h/2)

        frameArea = h*w
        print("Area do Frame:", frameArea)
        areaTH = frameArea/225
        print ('Area Threshold', areaTH) # Area de contorno usada para detectar uma pessoa

        #Linhas de Entrada/Saída

        #line_up = int(2.25*(h/6))
        #line_down   = int(3.75*(h/6))
        line_up = int(2*(h/6))    #deve-se adaptar de acordo com as caracteristicas da camera
        line_down = int(2*(h/6))  #deve-se adaptar de acordo com as caracteristicas da camera
        print ("Line UP:", line_up)
        print ("Line DOW:", line_down)

        up_limit =   int(1*(h/6))
        down_limit = int(5*(h/6))

        print ("Limite superior:", up_limit)
        print ("Limite inferior:", down_limit)

        #Propriedades das linhas

        print ("Red line y:",str(line_down))
        print ("Blue line y:", str(line_up))
        line_down_color = (0,0,255)
        line_up_color = (255,0,0)
        pt1 =  [0, line_down];
        pt2 =  [w, line_down];
        pts_L1 = np.array([pt1,pt2], np.int32)
        pts_L1 = pts_L1.reshape((-1,1,2))
        pt3 =  [0, line_up];
        pt4 =  [w, line_up];
        pts_L2 = np.array([pt3,pt4], np.int32)
        pts_L2 = pts_L2.reshape((-1,1,2))

        pt5 =  [0, up_limit];
        pt6 =  [w, up_limit];
        pts_L3 = np.array([pt5,pt6], np.int32)
        pts_L3 = pts_L3.reshape((-1,1,2))
        pt7 =  [0, down_limit];
        pt8 =  [w, down_limit];
        pts_L4 = np.array([pt7,pt8], np.int32)
        pts_L4 = pts_L4.reshape((-1,1,2))

        #Substrator de fundo
        fgbg = cv2.createBackgroundSubtractorMOG2(500,detectShadows = True)

        #Elementos estruturantes para filtros morfoogicos
        kernelOp = np.ones((3,3),np.uint8)
        kernelOp2 = np.ones((5,5),np.uint8)
        kernelOp3 = np.ones((8, 8), np.uint8)
        kernelCl = np.ones((11,11),np.uint8)
        kernelCl2 = np.ones((8, 8), np.uint8)

        #Inicialização de variaveis Globais
        font = cv2.FONT_HERSHEY_SIMPLEX
        pessoas = []
        max_p_age = 5
        pid = 1

        while(cap.isOpened()):
            ##for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            #Lê uma imagem de uma fonte de video


            ret, frame = cap.read()
            ## frame = image.array


            for pessoa in pessoas:
                pessoa.age_one() #age every person one frame
            #########################
            #   PRE-PROCESSAMENTO   #
            #########################

            #Aplica subtração de fundo
            fgmask = fgbg.apply(frame)
            fgmask2 = fgbg.apply(frame)

            #Binarização para eliminar sombras (color gris)
            try:
                ret,imBin= cv2.threshold(fgmask,128,255,cv2.THRESH_BINARY)
                ret,imBin2 = cv2.threshold(fgmask2,128,255,cv2.THRESH_BINARY)
                #Opening (erode->dilate) para remover o ruído.
                mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
                mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)
                #Closing (dilate -> erode) para juntar regiões brancas.
                mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
                mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)
            except:
                print('EOF')
                print ('Entrou:',cnt_up)
                print ('Saiu:',cnt_down)
                return (cnt_up - cnt_down)
                #break
            #################
            #   CONTORNOS   #
            #################

            # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
            _, contours0, hierarchy = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours0:
                area = cv2.contourArea(cnt)
                #cv2.drawContours(frame, cnt, -1, (0,0,255), 3, 8)
                if area > areaTH:
                    #####################
                    #   RASTREAMENTO    #
                    #####################

                    #Falta agregar condições para multiplas pessoas, saídas e entradas da tela

                    M = cv2.moments(cnt)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    x, y, w, h = cv2.boundingRect(cnt)

                    # tentativa de remover retangulos muito largos
                    #if(x >= 240 or h >= 240):
                    #   continue

                    new = True
                    if cy in range(up_limit,down_limit):
                        #print(x, y, w, h)
                        for pessoa in pessoas:
                            if abs(cx - pessoa.getX()) <= w and abs(cy - pessoa.getY()) <= h:
                                # O objeto está perto de um que já foi detectado anteriormente
                                new = False
                                pessoa.updateCoords(cx,cy)   #atualizar coordenadas no objeto e reseta a idade
                                if pessoa.deslocaCima(line_down,line_up) == True:
                                    cnt_up += 1;
                                    print ("ID: ",pessoa.getId(),'Entrou às',time.strftime("%c"))
                                    print("Area objeto: " + str(area))
                                elif pessoa.deslocaBaixo(line_down,line_up) == True:
                                    cnt_down += 1;
                                    print ("ID: ",pessoa.getId(),'Saiu às',time.strftime("%c"))
                                    print("Area objeto: " + str(area))
                                break
                            if pessoa.getState() == '1':
                                if pessoa.getDir() == 'Saiu' and pessoa.getY() > down_limit:
                                    pessoa.setDone()
                                elif pessoa.getDir() == 'Entrou' and pessoa.getY() < up_limit:
                                    pessoa.setDone()
                            if pessoa.timedOut():
                                #remover pessoas da lista
                                index = pessoas.index(pessoa)
                                pessoas.pop(index)
                                del pessoa #libera a memoria de variavel i.
                        if new == True:
                            p = Pessoa.Pessoa(pid, cx, cy, max_p_age)
                            pessoas.append(p)
                            pid += 1
                    #################
                    #   DESENHOS    #
                    #################
                    cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
                    img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                    #cv2.drawContours(frame, cnt, -1, (0,255,0), 3)

            #END for cnt in contours0

            #########################
            # DESENHAR TRAJETÓRIAS  #
            #########################
            for pessoa in pessoas:
                if len(pessoa.getTracks()) >= 2:
                   pts = np.array(pessoa.getTracks(), np.int32)
                   pts = pts.reshape((-1,1,2))
                   frame = cv2.polylines(frame,[pts],False,pessoa.getRGB())
                if pessoa.getId() == 9:
                   print (str(pessoa.getX()), ',', str(pessoa.getY()))
                cv2.putText(frame, str(pessoa.getId()),(pessoa.getX(),pessoa.getY()),font,0.3,pessoa.getRGB(),1,cv2.LINE_AA)

            #################
            #   IMAGEM      #
            #################
            str_up = 'Entraram '+ str(cnt_up)
            str_down = 'Sairam '+ str(cnt_down)
            tituloup = "Entrada "
            titulodown = "Saida "
            dataehora = time.strftime("%c")
            frame = cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
            #frame = cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
            #frame = cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
            #frame = cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)

            self.escreveCabecalho(frame, str_up, str_down, titulodown,tituloup,dataehora,font, x_meio)

            cv2.imshow('Frame',frame)
            cv2.imshow('Debug',mask)

            #preisonar ESC para sair
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        #END while(cap.isOpened())

        #################
        #   LIMPEZA     #
        #################
        cap.release()
        cv2.destroyAllWindows()

    def escreveCabecalho(self,frame,str_up, str_down, titulodown, tituloup, dataehora, font, x_meio):
        cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 60), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 60), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, tituloup, (x_meio, 20), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, titulodown, (x_meio, 450), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, dataehora, (420, 20), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

if __name__ == '__main__':
    c = Contador()
    c.detectPeople()