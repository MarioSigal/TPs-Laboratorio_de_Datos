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
    etiqueta = ['Remera/top', 'Pantalones', 'Suéter', 'Vestido', 'Abrigo', 'Sandalias', 'Camisa', 'Zapatillas', 'Cartera', 'Botas', 'Promedio']
    data = df.values
    pixel_values = data[num_fila][1:]
    
    # Convertir los valores de píxeles a una matriz de 28x28
    image_array = np.array(pixel_values).reshape(28, 28) 
    
    # Mostrar la imagen usando matplotlib
    plt.imshow(image_array, cmap='gray')  # 'gray' para mostrar la imagen en escala de grises
    plt.title(etiqueta[data[num_fila][0]])
    plt.axis('off')
    plt.show()

#%%

visualizar_prenda(fashion_mnist,1)
#%%
# Ejercicio 1
# a) ¿Cuáles parecen ser atributos relevantes para predecir el tipo de prenda?
# ¿Cuáles no? ¿Creen que se pueden descartar atributos?


primer_pixel = fashion_mnist[['pixel1']]
ultimo_pixel = fashion_mnist[['pixel784']]

primer_pixel['pixel1'].unique()         #este capaz se puede sacar
len(primer_pixel['pixel1'].unique())

# pixel 2 tiene 17 
ultimo_pixel['pixel784'].unique()
len(ultimo_pixel['pixel784'].unique())

del primer_pixel, ultimo_pixel

#contamos 0s
zero_counts = np.sum(fashion_mnist == 0, axis=0)
ax = zero_counts.plot.bar().set(title='cantidad de 0s')
ax.plt.xlabel('pixeles')
ax.plt.ylabel('Cantidad de ceros')
ax.plt.show()
ax.plt.close()

del ax
# Crear un gráfico de barras para representar la cantidad de ceros en cada columna

# Imagen promedio 
etiqueta = ['Remera/top', 'Pantalones', 'Suéter', 'Vestido', 'Abrigo', 'Sandalias', 'Camisa', 'Zapatillas', 'Cartera', 'Botas']
for j in range(10):
    prenda = fashion_mnist[fashion_mnist['label'] == j]
    imagen = np.zeros(784)
    for i in range(1, 785):
        imagen[i-1] = prenda[f'pixel{i}'].mean()
    plt.title(etiqueta[j])
    image_array = np.array(imagen).reshape(28, 28) 
    plt.imshow(image_array, cmap='plasma')  
    plt.axis('off')
    plt.show()




fashion_mnist_promedios = pd.DataFrame()
fashion_mnist_promedios['label'] = 10 
for i in range(1,785):
    fashion_mnist_promedios[f'pixel{i}'] = [fashion_mnist[f'pixel{i}'].mean()]
# Imagen desvio estandar ()


imagen = np.zeros(784)
for i in range(1, 785):
    imagen[i-1] = fashion_mnist_promedios[f'pixel{i}']
image_array = np.array(imagen).reshape(28, 28) 
plt.imshow(image_array, cmap='plasma')  
plt.axis('off')
plt.show()




#grafico??


del primer_pixel, ultimo_pixel
#%%
# b) ¿Hay clases de prendas que son parecidas entre sí? Por ejemplo, ¿Qué es 
# más fácil de diferenciar: remeras de pantalones o remeras de pullovers?


remera = fashion_mnist[fashion_mnist['label'] == 2]

#%%
# c) Tomen una de las clases, por ejemplo vestidos, ¿Son todos muy similares entre sí?