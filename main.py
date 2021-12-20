from enviroment import build_env
from sensor import sensor_LiDAR
import pygame as pyg
import math
import numpy as np

enviroment = build_env((1200,600))                                  # Instaciação do Ambiente

enviroment.env_Map = enviroment.Map.copy()                          # copia ambiente para env_Map
err = [float( 0.4), float(0.01)]                                    # error - ruido set
laser = sensor_LiDAR(200, enviroment.env_Map, err)                  # Instanciação Sensor - recebe mapa para a percepção
enviroment.Map.fill((0,0,0))
enviroment.infoMap = enviroment.Map.copy()

running = True

while running:
    sensorON = False
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
        if pyg.mouse.get_focused():                             # mouse só é lido caso esteja na janela da simulação : sensorON
            sensorON = True
        else:
            sensorON = False
    
    if sensorON:
        position = pyg.mouse.get_pos()                                  # pega posição do mouse
        #print(position)
        laser.position = position                                       # atualiza posição do sensor com a posição do mouse
        sensor_data = laser.senseObjects()                              # função sensorial
        print(sensor_data)
        enviroment.pointCloudStorage(sensor_data, position)             # guarda os dados de sensor na abstração do ambiente
        enviroment.showPointCloud()                                     # mostra os pontos coletados pelo sensor na tela
    enviroment.Map.blit(enviroment.infoMap, (0,0))                      # o InfoMAp é a estrutura que possibilita a visualização dos pontos
    pyg.display.update()                                                # update do display