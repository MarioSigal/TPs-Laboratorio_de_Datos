# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 01:46:38 2023

@author: mario
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


fashion_mnist = pd.read_csv('./fashion-mnist.csv')
#%% Descripción del data set

# cantidad de datos: 60.000

# cantidad de atributos: 785

# tipos de atributo:el primer atributo ('label') corresponde a una clasificacion por tipo de prenda que aparece en la imagen; 
#                   los siguientes 784 atributos corresponden al valor de cada pixel de la imagen en una escala de grices de 0 a 255


# la clasificacion dada por el atributo 'label' significa:
# 0 Camiseta/top
# 1 Pantalón
# 2 Pullover
# 3 Vestido
# 4 Abrigo
# 5 Sandalia
# 6 Camisa
# 7 Zapatilla
# 8 Bolsa
# 9 Bota de tobillo
# =============================================================================



#%%
#Visualizacion de imagenes
# Convertir el DataFrame a un NumPy array
data = fashion_mnist.values

# Iterar a través de las filas del array y mostrar cada imagen
for i in range(len(data)-59900):
    # Obtener los valores de píxeles para la imagen actual
    pixel_values = data[i][1:]
    
    # Convertir los valores de píxeles a una matriz de 28x28
    image_array = np.array(pixel_values).reshape(28, 28) 
    
    # Mostrar la imagen usando matplotlib
    plt.imshow(image_array, cmap='gray')  # 'gray' para mostrar la imagen en escala de grises
    plt.title(f'Imagen {i + 1}')
    plt.axis('off')
    plt.show()
# del para borrar las variables que ya no son usadas    
del data, i, image_array, pixel_values 
#%%
