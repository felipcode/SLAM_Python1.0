import math
import pygame as pyg

class build_env:

    def __init__(self, Mapdimentions):
        pyg.init()                                                              # biblioteca pyg
        self.pointCloud=[]                                                      # Array nuvem de ptos
        self.env_Map = pyg.image.load('resources\map1.png')                     # Load do Mapa
        self.map_h, self.map_w = Mapdimentions                                  
        self.MapWindowName = 'SLAM SIMULATION'
        pyg.display.set_caption(self.MapWindowName)
        self.Map = pyg.display.set_mode((self.map_h, self.map_w))       # set the display heigh x whidth
        self.Map.blit(self.env_Map, (0,0))

                                    # Declaration of COLORS
        self.black = (0,0,0)
        self.green = (0,255,0)
        self.grey = (70,70,70)
        self.white = (255,255,255)
        self.red = (255,0,0)
        
    def to_cartesian2D(self, distance, angle, mousePosition):       # Tem como entrada a distancia e angulo recebidos   (sist. coordenadas com origem no sensor)
        x = distance*math.cos(angle)+mousePosition[0]               # do sensor e a posição espacial do sensor(mouse)
        y = -distance*math.sin(angle)+mousePosition[1]              # fica negativo pois usa seno , entao para nao alterar angle computa-se assim
        print(x,y)
        return (int(x), int(y))

    def pointCloudStorage(self, data, pos):                                             # Recebe os dados do sensor, converte p/
                                                                                        # coordenadas cartesianas e guarda na 
        if data!=False:                                                                 # variável self.pointCloud
            for element in data:                                                           
                point = self.to_cartesian2D(element[0], element[1], pos)                    
                if point not in self.pointCloud:
                    self.pointCloud.append(point)    

    def showPointCloud(self):                                                         # print pontos
        self.infoMap = self.Map.copy()
        for point in self.pointCloud:
            self.infoMap.set_at(((int(point[0])), (int(point[1]))), (255, 255, 0))    # InfoMap é mapeado de acordo com
                                                                                      # as coordenadas da nuvem de pontos   
                                                                                      # "entregue" pelo sensor