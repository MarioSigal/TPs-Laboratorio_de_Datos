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
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
#%%
# Importación de datos

fashion_mnist = pd.read_csv('./fashion-mnist.csv')
fashion_mnist.head()

#%%
# Definición de funciones

# función que trasforma la fila de una prenda en específico, con sus 784 
# pixeles, en una imagen. 0 <= num_fila < 60000
def visualizar_prenda(num_fila):
    etiqueta = ['Remera/top', 'Pantalones', 'Suéter', 'Vestido', 'Abrigo', 'Sandalias', 'Camisa', 'Zapatillas', 'Cartera', 'Botas']
    data = fashion_mnist.values
    pixel_values = data[num_fila][1:]
    
    # Convertir los valores de píxeles a una matriz de 28x28
    image_array = np.array(pixel_values).reshape(28, 28) 
    
    # Mostrar la imagen usando matplotlib
    plt.imshow(image_array, cmap='gray')  # 'gray' para mostrar la imagen en escala de grises
    plt.title(etiqueta[data[num_fila][0]])
    plt.axis('off')
    plt.show()
  
    
#%%
visualizar_prenda(425)

#%%
# Exploración del dataframe
fashion_mnist.info() # cantidad de filas, columnas y tipo de datos
fashion_mnist['label'].unique() # cuántas son las labels
fashion_mnist['label'].value_counts() # qué cantidad hay de cada categoría
#%%
# Imagen promedio de cada prenda
fashion_mnist_promedios_prenda = pd.DataFrame()
etiqueta = ['Remera/top', 'Pantalones', 'Suéter', 'Vestido', 'Abrigo', 'Sandalias', 'Camisa', 'Zapatillas', 'Cartera', 'Botas']
for j in range(10):
    prenda = fashion_mnist[fashion_mnist['label'] == j]
    fashion_mnist_promedios_prenda.at[j,'label'] = j
    imagen = np.zeros(784)
    for i in range(1, 785):
        fashion_mnist_promedios_prenda.at[j, f'pixel{i}'] = prenda[f'pixel{i}'].mean()
        imagen[i-1] = prenda[f'pixel{i}'].mean()
    plt.title(etiqueta[j])
    image_array = np.array(imagen).reshape(28, 28) 
    plt.imshow(image_array, cmap='plasma')  
    plt.axis('off')
    plt.show()

del imagen, prenda, j, i, image_array
#%%
# Nuevo dataFrame con los valores promedio de todas las prendas juntas
fashion_mnist_promedios = pd.DataFrame()
fashion_mnist_promedios['label'] = [10] 
for i in range(1,785):
    fashion_mnist_promedios[f'pixel{i}'] = [fashion_mnist[f'pixel{i}'].mean()]

del i 
#%%
# Imagen de los valores promedios de todas las prendas juntas
etiqueta = ['Remera/top', 'Pantalones', 'Suéter', 'Vestido', 'Abrigo', 'Sandalias', 'Camisa', 'Zapatillas', 'Cartera', 'Botas']
imagen_prom = np.zeros(784)
for i in range(1, 785):
    imagen_prom[i-1] = fashion_mnist_promedios[f'pixel{i}']
image_array = np.array(imagen_prom).reshape(28, 28) 
plt.title('Imagen promedio')
plt.imshow(image_array, cmap='Blues')  
plt.axis('off')
plt.show()

del etiqueta, i, image_array, imagen_prom
#%%
# b) ¿Hay clases de prendas que son parecidas entre sí? Por ejemplo, ¿Qué es 
# más fácil de diferenciar: remeras de pantalones o remeras de pullovers?

# Representación visual de la comparación entre dos prendas promedio, pantalones y zapatillas 
# Imagenes superpuestas
etiqueta = ['Remera/top', 'Pantalones', 'Suéter', 'Vestido', 'Abrigo', 'Sandalias',
            'Camisa', 'Zapatillas', 'Cartera', 'Botas']

num_fila1 = 1 #pantalones
num_fila2 = 7 #zapatillas

data = fashion_mnist_promedios_prenda.values
pixeles1 = data[num_fila1][1:]
imagen1 = np.array(pixeles1).reshape(28, 28)
pixeles2 = data[num_fila2][1:]
imagen2 = np.array(pixeles2).reshape(28, 28)
plt.imshow(imagen1, cmap='Grays')  
plt.axis('off')
plt.imshow(imagen2, cmap='Blues', alpha=0.5)  
plt.axis('off')
plt.title(f'{etiqueta[int(data[num_fila1][0])]} vs {etiqueta[int(data[num_fila2][0])]}')
plt.show()

# Calculo de promedio de filas, para poder visualizar 28 valores en vez de 784
prom_filas1 = np.zeros(28)
prom_filas2 = np.zeros(28)
j = 0
for i in range(1,758,28):
    prom1 = data[num_fila1][i:i+27].mean()
    prom2 = data[num_fila2][i:i+27].mean()
    prom_filas1[j] = prom1
    prom_filas2[j] = prom2
    j += 1

# Grafico de los valores de promedios de las filas de ambas prendas
sns.scatterplot(x=np.arange(1,29), y=prom_filas1)
sns.scatterplot(x=np.arange(1,29), y=prom_filas2).set(
                    title='Tonalidad promedio por fila de pantalones y zapatillas', 
                    xlabel='fila de imagen', ylabel='promedio de fila de pixeles')
plt.xticks(np.arange(0,29,2))
plt.legend(labels=['pantalones', 'zapatillas'], title='prenda')


# Representación visual de la comparación entre suéter y camisa
# Imagenes superpuestas
num_fila1 = 2 #suéter
num_fila2 = 6 #camisa

pixeles1 = data[num_fila1][1:]
imagen1 = np.array(pixeles1).reshape(28, 28)
pixeles2 = data[num_fila2][1:]
imagen2 = np.array(pixeles2).reshape(28, 28)
plt.imshow(imagen1, cmap='Grays')  
plt.axis('off')
plt.imshow(imagen2, cmap='Blues', alpha=0.5)  
plt.axis('off')
plt.title(f'{etiqueta[int(data[num_fila1][0])]} vs {etiqueta[int(data[num_fila2][0])]}')
plt.show()

# Calculo de promedio de filas, para poder visualizar 28 valores en vez de 784
prom_filas1 = np.zeros(28)
prom_filas2 = np.zeros(28)
j = 0
for i in range(1,758,28):
    prom1 = data[num_fila1][i:i+27].mean()
    prom2 = data[num_fila2][i:i+27].mean()
    prom_filas1[j] = prom1
    prom_filas2[j] = prom2
    j += 1
    
# Grafico de los valores de promedios de las filas de ambas prendas
sns.scatterplot(x=np.arange(1,29), y=prom_filas1)
sns.scatterplot(x=np.arange(1,29), y=prom_filas2).set(
                    title='Tonalidad promedio por fila de suéter y camisa', 
                    xlabel='fila de imagen', ylabel='promedio de fila de pixeles')
plt.xticks(np.arange(0,29,2))
plt.legend(labels=['suéter', 'camisa'], title='prenda')

# =============================================================================
# Conclusión:
#     con la visualización por imagen de la comparación de dos prendas promedio, 
#     se puede apreciar las diferencias entre las catégorias. Entre el pantalón y 
#     las zapatillas se puede ver que en la parte superior e inferior de la figura 
#     de los pantalones, estos se ven solos, y solo en el medio se superponen las 
#     dos figuras. Lo mismo con los costados de la zapatilla. Por esto, estas dos 
#     prendas son fáciles de diferenciar. Pero si se compara suéter y camisa, casi 
#     que no hay diferencias.
# =============================================================================

del num_fila1, num_fila2, data, imagen1, imagen2, pixeles1, pixeles2, etiqueta
del i, j, prom1, prom2, prom_filas1, prom_filas2
#%%
# c) Tomen una de las clases, por ejemplo vestidos, ¿Son todos muy similares entre sí?

# Imagenes de desvio estandar de todas las prendas
etiqueta = ['Remera/top', 'Pantalones', 'Suéter', 'Vestido', 'Abrigo', 'Sandalias',
            'Camisa', 'Zapatillas', 'Cartera', 'Botas']

for j in range(10):
    prenda = fashion_mnist[fashion_mnist['label'] == j]
    imagen = np.zeros(784)
    for i in range(1, 785):
        imagen[i-1] = prenda[f'pixel{i}'].std()
    plt.title(etiqueta[j])
    image_array = np.array(imagen).reshape(28, 28) 
    plt.imshow(image_array, cmap='plasma')  
    plt.axis('off')
    plt.show()
    
# Visualizacion del desvio de sandialias
# Comparación del promedio de las filas del promedio general, con el promedio 
# de las filas de 10 sandalias al azar
data1 = fashion_mnist_promedios_prenda.values
num_fila = 5 # sandalias
prom_filas1 = np.zeros(28)
j = 0
for i in range(1,758,28):
    prom = data1[num_fila][i:i+27].mean()
    prom_filas1[j] = prom
    j += 1

data2 = fashion_mnist[fashion_mnist['label'] == 5].values
data2 = data2[:10,1:]
prom_filas2 = np.zeros((10,28))

for k in range(10):
    j = 0
    for i in range(1,758,28):
        prom = data2[k][i:i+27].mean()
        prom_filas2[k,j] = prom
        j += 1

sns.scatterplot(x=np.arange(1,29), y=prom_filas1).set(
                        title='Tonalidad promedio por fila de 10 sandalias contra el promedio', 
                        xlabel='fila de imagen', ylabel='promedio de pixel')
for i in range(10):
    sns.scatterplot(x=np.arange(1,29), y=prom_filas2[i,:], marker='x')

plt.xticks(np.arange(0,29,2))
plt.legend(labels=['promedio de todas las sandalias'])


# Visualizacion del desvio de pantalones
# Comparación del promedio de las filas del promedio general, con el promedio 
# de las filas de 10 pantalones al azar
data1 = fashion_mnist_promedios_prenda.values
num_fila = 1 # pantalones
prom_filas1 = np.zeros(28)
j = 0
for i in range(1,758,28):
    prom = data1[num_fila][i:i+27].mean()
    prom_filas1[j] = prom
    j += 1

data2 = fashion_mnist[fashion_mnist['label'] == 1].values
data2 = data2[:10,1:]
prom_filas2 = np.zeros((10,28))

for k in range(10):
    j = 0
    for i in range(1,758,28):
        prom = data2[k][i:i+27].mean()
        prom_filas2[k,j] = prom
        j += 1

sns.scatterplot(x=np.arange(1,29), y=prom_filas1).set(
                        title='Tonalidad promedio por fila de 10 pantalones contra el promedio', 
                        xlabel='fila de imagen', ylabel='promedio de pixel')
for i in range(10):
    sns.scatterplot(x=np.arange(1,29), y=prom_filas2[i,:], marker='x')

plt.xticks(np.arange(0,29,2))
plt.legend(labels=['promedio de todos los pantalones'])


del data1, data2, etiqueta, i, image_array, imagen, j, k, num_fila, prenda, prom
del prom_filas1, prom_filas2
#%%
# Sacamos los pixeles que en promedio son cercanos a 0

fashion_mnist_limpio = fashion_mnist
columnas_0 = []
for i in range(1,fashion_mnist_promedios.shape[1]):
    if fashion_mnist_promedios.at[0, f'pixel{i}'] < 1:
        columnas_0.append(f'pixel{i}')
        
fashion_mnist_limpio = fashion_mnist_limpio.drop(columns = columnas_0)

del columnas_0, i 
    
#%%
# Ejercicio 2 a)
remeras_pantalones = fashion_mnist_limpio[fashion_mnist['label'] <= 1]

# b)
remeras_pantalones['label'].value_counts() # sí, esta balanceado

X = remeras_pantalones.drop(columns = ['label'])
y = remeras_pantalones[['label']]


X_train, X_test, y_train, y_test = train_test_split(X, y , test_size= 0.15, random_state= 7, stratify= y)

# c)
# 3 con 3 atributos
# 3 con 20
# 1 con 6
# 3 con 377
# 3 con 183
# 3 con 560

# Capaz que elegimos muchos conjuntos de distintos atributos para comparar
# Habría que consultar cuántos masomenos están bien


# CORREGIR Y CALCULAR LOS PROMEDIOS CON EL DATAFRAME LIMPITO O SACARLE TODO LO QUE SEA MENOR A 1
# 3 atributos
# Media max remeras, media max pantalones, maxima diferencia promedio entre la media de dos pixeles
pixel_max_remeras = fashion_mnist_promedios_prenda[fashion_mnist_promedios_prenda['label']==0].idxmax(axis='columns')
print(pixel_max_remeras)
pixel_max_pantalones = fashion_mnist_promedios_prenda[fashion_mnist_promedios_prenda['label']==1].idxmax(axis='columns')
print(pixel_max_pantalones)
max_dif = fashion_mnist_promedios_prenda[fashion_mnist_promedios_prenda['label'] <= 1].diff(axis=0).idxmax(axis='columns')
print(max_dif)

max_medias= X_train[['pixel14', 'pixel42', 'pixel45']]

# =============================================================================
# Media minima de remeras, media minima de pantalones, minima diferencia promedio entre la media de dos pixeles
pixel_min_remeras = fashion_mnist_promedios_prenda[fashion_mnist_promedios_prenda['label'] == 0].drop(columns=['label']).idxmin(axis='columns')
print(pixel_min_remeras)
pixel_min_pantalones = fashion_mnist_promedios_prenda[fashion_mnist_promedios_prenda['label']==1].idxmin(axis='columns')
print(pixel_min_pantalones)
min_dif = fashion_mnist_promedios_prenda[fashion_mnist_promedios_prenda['label'] <= 1].diff(axis=0).idxmin(axis='columns')
print(min_dif)

max_medias= X_train[['pixel1', 'pixel', 'pixel743']]

## PARA HACER ESTO DEBERÏAMOS LIMPIAR EL DATAFRAME DE PROMEDIOS Y DESCARTAR TODO AQUELLO QUE FUERA 0 O RECALCULAR CON EL LIMPITO


# =============================================================================
# Maxima diferencia y minima diferencia promedio, algo más...




# 6 atributos

# Cuartiles remeras y cuartiles pantalones

# para mas de un atributo podemos hacer un slice en la distribución

# Para el KNN vamos a trabajar primero

# Búsqueda de la mejor cantidad de vecinos
hyper_params = {'n_neighbors' : [4,5,6,7,8,9,10,11,12]}
neigh = KNeighborsRegressor()
clf = GridSearchCV(estimator=neigh, param_grid=hyper_params, cv = 5)
search = clf.fit(X_train, y_train)
search.best_params_
search.best_score_

# d)

# e)

del X, y, X_train, X_test, y_train, y_test
#%%
# Ejercicio 3 a)
# Dividimos en data train y data test 

X = fashion_mnist_limpio.drop(columns = ['label'])
y = fashion_mnist[['label']]

X_train, X_test, y_train, y_test = train_test_split(X, y , test_size= 0.20, random_state= 7, stratify= y)
#%%
# Armamos el modelo y evaluamos cuál conviene más

# Preguntas, cuántos k-folds nos convienen
# Como podemos razonar el rango de altura en que se mueven los arboles
# Con esto ya estaría
hyper_params = {'criterion' :["gini", "entropy"], 'max_depth' : [4,5,6,7,8,9,10,11,12]}
arbol = DecisionTreeClassifier()
clf = GridSearchCV(estimator=arbol, param_grid=hyper_params, cv = 5)
search = clf.fit(X_train, y_train)
search.best_params_
search.best_score_

del arbol
#%%

arbol=DecisionTreeClassifier(criterion='mejor criterio', max_depth='mejor profundidad')
arbol.predict(X_test, y_test)

# Medir precisión y recall???
del X, y, X_train, X_test, y_train, y_test

















