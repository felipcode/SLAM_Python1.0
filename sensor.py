import math
import numpy as np
import matplotlib
import pygame as pyg

def noise_gauss(distance, angle, sigma):                # add's uncertainty
    mean = np.array([distance, angle])
    covariance = np.diag(sigma**2)
    distance, angle = np.random.multivariate_normal(mean, covariance)
    distance = max(distance, 0)
    angle = max(angle, 0)
    return [distance, angle]



class sensor_LiDAR:
    def __init__(self, range, Map, uncertainty):                        # Recebe uma instancia do mapa real para detectar objetos no ambiente
        self.range = range
        self.rotation_fixed_speed = 4                                   # a velocidade de rotação na simulação é na verdade a velocidade dos laços de repetição
        self.sigma = np.array(uncertainty)
        self.position = (0,0)
        self.map = Map                                                  # instancia o mapa dentro da classe para obter as percepções --
        self.w, self.h = pyg.display.get_surface().get_size()
        print(self.w, self.h)
        self.senseObject=[]

    def distance(self, Obj_position):                                                       # calcula distancia [x,y] teorema pitágoras
        px = (Obj_position[0] - self.position[0]) **2
        py = (Obj_position[1] - self.position[1]) **2
        return math.sqrt(px+py)

    def senseObjects(self):
        data = []                                                                                   # data : armazena (r, theta)
        x1, y1 = self.position[0], self.position[1]                                                 # pos mouse
        for angle in np.linspace(0, 2*math.pi, 540, False):                                         # angular variation 0° to 2*pi(360°) angular resolution 0.50° 
            x2, y2 = (x1 + self.range*math.cos(angle)), (y1 - self.range*math.sin(angle))           # x2,y2 percorrem a direção estabelecida pela orientação do angulo "atual" do sensor - theta
            # print(x2,y2)
            # sampling loop - amostragem ::
            for i in range(0, 100):                                                      # amostragem dos pulsos/ divide x2 e y2 em 100 "pontos amostrais"
                u = i/100  # parametro amostragem
                                                                                            # Interpolação
                x = int(x2*u + x1*(1-u))
                y = int(y2*u + y1*(1-u))

                if  ((0 < x < self.w) and (0 < y < self.h)):
                    color = self.map.get_at((x, y))
                    print(color)
                    if ((color[0], color[1], color[2]) == (0,0,0)):                         # Compara a cor
                        
                        distance = self.distance((x, y))                                    # computa a distancia
                        output = noise_gauss(distance, angle, self.sigma)                   # ruidos 
                        data.append(output)                                                 # armazena em self.data caso seja "ponto de reflexão"
                        break
        if len(data) > 0:
            return data                                                                     # retorna um array de coordenadas com a origem no sensor
        else:
            return False
