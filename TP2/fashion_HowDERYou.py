#%%

"""
Grupo: "How DER You?"
Integrantes: Mario Sigal Aguirre, Augusto Guarnaccio, Azul Barracchia
Contenido...
"""

#%%
# Importación de bibliotecas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn 

#%%
# Importación de datos

fashion_mnist = pd.read_csv('./fashion-mnist.csv')

#%%
# Definición de funciones

# función que trasforma la fila de una prenda en específico, con sus 784 
# pixeles, en una imagen. 0 <= num_fila < 60000
def visualizar_prenda(df, num_fila):
    data = df.values
    pixel_values = data[num_fila][1:]
    
    # Convertir los valores de píxeles a una matriz de 28x28
    image_array = np.array(pixel_values).reshape(28, 28) 
    
    # Mostrar la imagen usando matplotlib
    plt.imshow(image_array, cmap='gray')  # 'gray' para mostrar la imagen en escala de grises
    plt.title(f'Imagen {num_fila + 1}')
    plt.axis('off')
    plt.show()

#%%

visualizar_prenda(fashion_mnist, 9999)

#%%
# Ejercicio 1
# a) ¿Cuáles parecen ser atributos relevantes para predecir el tipo de prenda?
# ¿Cuáles no? ¿Creen que se pueden descartar atributos?

primer_pixel = fashion_mnist[['pixel1']]
ultimo_pixel = fashion_mnist[['pixel784']]

primer_pixel['pixel1'].unique()         #este capaz se puede sacar
len(primer_pixel['pixel1'].unique())

ultimo_pixel['pixel784'].unique()
len(ultimo_pixel['pixel784'].unique())

#grafico??


del primer_pixel, ultimo_pixel
#%%
# b) ¿Hay clases de prendas que son parecidas entre sí? Por ejemplo, ¿Qué es 
# más fácil de diferenciar: remeras de pantalones o remeras de pullovers?


#%%
# c) Tomen una de las clases, por ejemplo vestidos, ¿Son todos muy similares entre sí?
