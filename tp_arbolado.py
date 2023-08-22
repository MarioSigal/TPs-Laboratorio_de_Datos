'''Definir una función leer_parque(nombre_archivo, parque) que abra el archivo
indicado y devuelva una lista de diccionarios con la información del parque especificado.
La lista debe tener un diccionario por cada árbol del parque elegido. Dicho diccionario
debe tener los datos correspondientes a un árbol (recordar que cada fila del csv
corresponde a un árbol).
Sugerencia: la columna que indica el parque se llama ‘espacio_ve’.'''

import csv
import numpy as np

nombre_archivo = "./arbolado-en-espacios-verdes.csv"

def leer_parque(nombre_archivo, parque):
    lista = armar_diccionario(nombre_archivo)
    listaRes = []
    for i in lista:
        if i["espacio_ve"] == parque:
            listaRes.append(i)
    return listaRes

def armar_diccionario (nombre_archivo): # Comentamos: comentario
    lista = []
    with open(nombre_archivo, 'rt') as f: 
        filas = csv.reader(f) 
        encabezado = next(filas) 
        for fila in filas: 
            registro = dict(zip(encabezado,fila))
            lista.append(registro)
    return lista

#print(len(leer_parque(nombre_archivo, "GENERAL PAZ")))
ej1 = leer_parque(nombre_archivo, "GENERAL PAZ")
ej11 = leer_parque(nombre_archivo, 'ANDES, LOS')
ej12 = leer_parque(nombre_archivo, 'CENTENARIO')

'''Escribir una función especies(lista_arboles) que tome una lista de árboles como la
generada en el ejercicio anterior y devuelva el conjunto de especies (la columna
'nombre_com' del archivo) que figuran en la lista.
Sugerencia: Usar el comando set.'''

def especies(lista_arboles):
    res = []
    for i in lista_arboles:
        res.append(i['nombre_com'])
    return set(res)

#print(especies(ej1))

'''Escribir una función contar_ejemplares(lista_arboles) que, dada una lista como la
generada con leer_parque(...), devuelva un diccionario en el que las especies sean
las claves y tengan como valores asociados la cantidad de ejemplares en esa especie en
la lista dada.
Debería verse que en el parque General Paz hay 20 Jacarandás, en el Parque Los Andes
hay 3 Tilos y en Parque Centenario hay 1 Laurel.'''

def contar_ejemplares(lista_arboles):
    res = {}
    for i in lista_arboles:
        if i['nombre_com'] in res.keys():
            res[i['nombre_com']] += 1
        else:
            res[i['nombre_com']] = 1
    return res

#print(contar_ejemplares(ej11)['Tilo'])

'''Escribir una función obtener_alturas(lista_arboles, especie) que, dada una lista
como la generada con leer_parque(...) y una especie de árbol (un valor de la
columna 'nombre_com' del archivo), devuelva una lista con las alturas (columna
'altura_tot') de los ejemplares de esa especie en la lista.
Observación: Conviene devolver las alturas como números (de punto flotante) y no como
cadenas de caracteres. Sugerimos hacer esto modificando leer_parque(...) o
modificando el tipo del valor antes de utilizarlo.
Usar la función para calcular la altura promedio y altura máxima de los 'Jacarandá' en
los tres parques mencionados. Debería obtenerse esto:'''


def obtener_alturas(lista_arboles, especie):
    lista = []
    for i in lista_arboles:
        if i['nombre_com'] == especie:
            lista.append(float(i['altura_tot']))
    return lista 

lista = obtener_alturas(ej1, 'Jacarandá')
max1 = max(lista)
prom = np.mean(lista)

#print(max1, prom)

'''Escribir una función obtener_inclinaciones(lista_arboles, especie) que, dada
una lista como la generada con leer_parque(...) y una especie de árbol, devuelva
una lista con las inclinaciones (columna 'inclinacio') de los ejemplares de esa
especie.'''

def obtener_inclinaciones(lista_arboles, especie):
    lista = []
    for i in lista_arboles:
        if i['nombre_com'] == especie:
            lista.append(float(i['inclinacio']))
    return lista 

#print(obtener_inclinaciones(ej1, 'Jacarandá'))

'''Combinando la función especies() con obtener_inclinaciones() escribir una
función especimen_mas_inclinado(lista_arboles) que, dada una lista de árboles
devuelva la especie que tiene el ejemplar más inclinado y su inclinación.
Correrlo para los tres parques mencionados anteriormente. Debería obtenerse, por
ejemplo, que en el Parque Centenario hay un Falso Guayabo inclinado 80 grados.'''

def especimen_mas_inclinado(lista_arboles):
    masInclinado = ''
    inclinacionMax = 0.0
    for especie in especies(lista_arboles):
        if inclinacionMax < max(obtener_inclinaciones(lista_arboles, especie)):
            masInclinado = especie
            inclinacionMax = max(obtener_inclinaciones(lista_arboles, especie))
    return masInclinado, inclinacionMax

#print(especimen_mas_inclinado(ej12))

'''Volver a combinar las funciones anteriores para escribir la función
especie_promedio_mas_inclinada(lista_arboles) que, dada una lista de árboles
devuelva la especie que en promedio tiene la mayor inclinación y el promedio calculado.
Resultados. Debería obtenerse, por ejemplo, que los Álamos Plateados del Parque Los
Andes tiene un promedio de inclinación de 25 grados.'''

def especie_promedio_mas_inclinada(lista_arboles):
    masInclinadoProm = ''
    inclinacionPromMax = 0.0
    for especie in especies(lista_arboles):
        if inclinacionPromMax < np.mean(obtener_inclinaciones(lista_arboles, especie)):
            masInclinadoProm = especie
            inclinacionPromMax = np.mean(obtener_inclinaciones(lista_arboles, especie))
    return masInclinadoProm, inclinacionPromMax

#print(especie_promedio_mas_inclinada(ej11))