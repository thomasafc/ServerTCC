import os
import zipfile
import numpy as np
import tensorflow as tf
import sys
import argparse
import cv2
import PIL
import matplotlib.pyplot as plt

from PIL import Image
from tensorflow import keras
from tensorflow.keras import layers
from matplotlib import image
from matplotlib import pyplot

train_size        = 1 # Tamanho dos dados para treinamento
max_vid_per_class = 1 # Número máximo de vídeos por classe
num_of_frames     = 12 # Número de frames que o vídeo será dividido
width             = 64 # Largura da imagem
height            = 48 # Altura da imagem
num_of_channels   = 1  # Número de canais da imagem (cinza, RGB, etc.)
num_of_classes    = 2  # Número de classes que serão utilizadas


def convertVideo(videoName):
    dataVideo = [] # armazena os frames

    # caminho do vídeo
    vid = str('./videoUpload/' + videoName)
    # lê o vídeo
    cap = cv2.VideoCapture(vid)
    frames = [] # armazenar os frames
    count = 0 # contador para pegar cada frame
    for j in range(num_of_frames): # aqui pegamos n frames de acordo com num_of_frames
        # 1000 = 1 segundo, 500 = meio segundo...
        cap.set(cv2.CAP_PROP_POS_MSEC,(count*250)) # seta o momento do vídeo para pegar o frame
        ret, frame = cap.read() # pega de fato o frame, e se deu sucesso ou não
        if ret == True: # se deu sucesso...
            print('S=>', end="")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # converte o frame para cinza
            frame = cv2.resize(frame,(width,height),interpolation=cv2.INTER_AREA) # redimensiona o frame
            frames.append(frame) # adiciona o frame para o vetor de frames
        else:
            print('*E*=>', end="")
        count = count + 1
    dataVideo.append(frames) # adiciona todos os frames de um vídeo
            
    dataVideo = np.array(dataVideo) # transforma o vetor de frames em array numpy
    print('\n\n===== FIM =====\n\n')

    # transforma os dados dos frames armazenados no formato ideal para ser usado na rede
    dataVideo = dataVideo.reshape(train_size, num_of_frames, width, height, num_of_channels)
    print(np.shape(dataVideo))


    # Retorna vetor com dados do video
    return dataVideo


def convertImage(imageName):
    dataImage = [] # Armazena os frames
    frames = [] # armazenar os frames

    # Pegando imagem
    frame = np.array(Image.open('./imageUpload/' + imageName))
    
    # Convertendo imagem para tons de cinza
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Redimencionsando Imagem
    frame = cv2.resize(frame,(width,height),interpolation=cv2.INTER_AREA)

    # adiciona o frame para o vetor de frames
    for i in range(num_of_frames):
        frames.append(frame)
    # adiciona todos os frames de um vídeo
    dataImage.append(frames)

    # Convertendo imagem para frames para ser usado na rede
    dataImage = np.array(dataImage)

    # transforma os dados dos frames armazenados no formato ideal para ser usado na rede
    dataImage = dataImage.reshape(train_size, num_of_frames, width, height, num_of_channels)
    print(np.shape(dataImage))

    # Retorna vetor com dados da imagem
    return dataImage

