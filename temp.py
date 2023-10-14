import pandas as pd
from inline_sql import sql, sql_val



operadores_organicos= pd.read_csv('./TablasOriginales/padron-de-operadores-organicos-certificados.csv')
# =============================================================================
#
# Listado de operadores orgánicos certificados:
#  
# incluye a: productores primarios, elaboradores y comercializadores.
#
# =============================================================================



establecimientos_productivos = pd.read_csv('./TablasOriginales/distribucion_establecimientos_productivos_sexo.csv')
# =============================================================================
#
# Distribución geográfica de los establecimientos productivos.
# 
# Base de datos que contiene coordenadas de los establecimientos productivos (no necesariamente orgánicos) con su 
# respectiva actividad económica, su nivel de empleo, jurisdicción y proporción de mujeres
#
# =============================================================================

localidades = pd.read_csv('./TablasOriginales/localidad_bahra.csv')
# =============================================================================
#
# Localidades de la Base de Asentamientos Humanos de la República Argentina
#
# Esta fuente permite asociar a la fuente primaria “Padrón de Operadores Orgánicos
# Certificados” con los datos de departamento. Lamentablemente la fuente primaria,
# en su campo departamento parece mezclar datos de departamento y ciudad, entre
# otras cosas. Esa fuente también tiene inconvenientes en cuanto al formato y
# escritura de los nombres (por ejemplo, no parecen contar con tildes, etc.). Deberán
# hacer lo necesario para curar y vincular los datos.
# 
# =============================================================================

clae = pd.read_csv('./TablasOriginales/clae_agg.csv')

# =============================================================================
# 
# Diccionario de CLAE: 
# 
# Dicha fuente contiene los nomencladores utilizados por AFIP
# para clasificar actividades con su correspondiente descripción.
# permite asociar a la fuente primaria “establecimiento productivo” los datos de actividades.
# 
# =============================================================================


# Ejercicio e)

df_Operadores_organicos = pd.DataFrame(columns=['establecimiento', 'razón_social', 'departamento', 'id_provincia', 'id_departamento'])
df_Producto = pd.DataFrame(columns=['producto', 'clae3']) 
df_Departamento = pd.DataFrame(columns=['id', 'departamento', 'id_provincia'])
df_Provincia = pd.DataFrame(columns=['id', 'provincia'])
df_Establecimiento_productivo = pd.DataFrame(columns=['id', 'clae2', 'proporción_mujeres'])
df_CLAE = pd.DataFrame(columns=['clae3','clae3_desc', 'clae2', 'clae2_desc'])
# relación entre operadores orgánicos y producto
df_Relacion_Produce = pd.DataFrame(columns=['establecimiento', 'razón_social', 'producto'])


# Ejercicio h) i)

# Limpieza 

# Limpieza operadores orgánicos
# =============================================================================
limpieza_operadores_organicos = """
                                SELECT REGEXP_REPLACE(establecimiento, '\\bNC\\b', 'ESTABLECIMIENTO ÚNICO') AS establecimiento, "razón social" AS razón_social,
                                    departamento, REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(productos,':',','), ' Y ',', '),'+',','),'-',','),'?',',') AS productos,
                                    provincia_id AS id_provincia
                                FROM operadores_organicos;
                                """
operadores_organicos = sql^limpieza_operadores_organicos

# =============================================================================
# Primero lo que se hizo fue empezar a limpiar/mejorar los datos 
# Para eso en la parte de establecimientos donde aparecía NC decidimos 
# Que diga establecimiento único (por qué)
# y también que las listas de productos solo aparezcan separadas por comas y no
# por otros caracteres no deseados
# =============================================================================


limpieza_operadores_organicos = """
                                SELECT *, TRIM(UNNEST( string_to_array(productos, ','))) AS producto
                                FROM operadores_organicos
                                """
operadores_organicos = sql^limpieza_operadores_organicos

# =============================================================================
# Después decidimos desglosar la lista de productos que aparecía para así 
# tenerlos todos por separado. Para esto usamos las funciones TRIM y UNNEST
# (explicar un poco que hace cada una)
# =============================================================================


limpieza_operadores_organicos = """
                                SELECT establecimiento, razón_social, departamento, id_provincia, REPLACE(REPLACE(REPLACE(producto, '(', ''), ')', ''), '.', '') AS producto
                                FROM operadores_organicos
                                ORDER BY id_provincia ASC
                                """
operadores_organicos = sql^limpieza_operadores_organicos
# =============================================================================
# Finalmente a la lista de productos decidimos ignorarla
# =============================================================================

# =============================================================================


# Limpieza localidades
# =============================================================================
limpieza_localidades = """
                        SELECT DISTINCT REPLACE(codigo_indec_departamento,'02001,02002,02003,02004,02005,02006,02007,02008,02009,02010,02011,02012,02013,02014,02015', '02001') AS id_departamento,
                            REPLACE(nombre_departamento,'Comuna 1,Comuna 10,Comuna 11,Comuna 12,Comuna 13,Comuna 14,Comuna 15,Comuna 2,Comuna 3,Comuna 4,Comuna 5,Comuna 6,Comuna 7,Comuna 8,Comuna 9', 'CIUDAD AUTONOMA BUENOS AIRES') AS departamento,
                            codigo_indec_provincia AS id_provincia, nombre_provincia AS provincia
                        FROM localidades                         
                        ORDER BY id_provincia ASC, id_departamento ASC
                        """
localidades = sql^limpieza_localidades   

# =============================================================================
# Primero decidimos hacer un SELECT DISTINCT para no tener localidades repetidas
# Luego nos quedamos solamente con: código que indica departamento,
# nombre de departamento, codigo que indica provincia, nombre de provincia.
# 
# Sin embargo, vimos que nos aparecían todas las columnas de CABA juntas así que
# decidimos juntarlas y renombrarlas como CABA y tomar un único índice para referirnos
# a estas. También apareció un problema de formato puesto que al final de la lista
# de comunas aparecía un espacio que luego dificultaba el acceso a ese valor por lo que
# decidimos borrarlo. 
#
# A su vez decidimos ordenar la tabla para que sea más fácil su lectura.
# =============================================================================

limpieza_localidades = """
                       SELECT id_departamento, id_provincia, provincia,
                           REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(UPPER(departamento),'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U') AS departamento
                       FROM localidades
                       """
localidades = sql^limpieza_localidades
# =============================================================================
# Por último decidimos deshacernos de las tildes para facilitar las búsquedas y 
# tener un criterio unificado
# =============================================================================

# Limpieza clae
# =============================================================================
limpieza_clae = """
                SELECT DISTINCT clae3, clae3_desc, clae2, clae2_desc
                FROM clae
                WHERE letra = 'A' or (letra = 'C' and clae2 in (10,11,12))
                ORDER BY clae2 ASC, clae3 ASC
              """
clae = sql^limpieza_clae

# =============================================================================
# Primero decidimos hacer un SELECT DISTINCT para no tener las repeticiones que se
# presentan en la tabla. Luego decidimos quedarnos con lo asociado a clae2 y clae3
# y además quedarnos solo con las claes asociadas a actividades del sector primario
# como también manufacturación de alimentos y derivados de productos orgánicos como
# pueden ser cremas (vamos a considerarlas como productos farmacéuticos)
# =============================================================================


# =============================================================================
# Limpieza establecimientos productivos
# =============================================================================
limpieza_establecimiento_productivo = """
                                        SELECT ID AS id, clae2, proporcion_mujeres
                                        FROM establecimientos_productivos
                                        ORDER BY id ASC
                                    """
establecimiento_productivo = sql^limpieza_establecimiento_productivo

# =============================================================================
# Decidimos quedarnos solamente con el id, la clasificación de clae2 y su proporción
# de mujeres, además de ordenar con por id ascendente
# =============================================================================

limpieza_establecimiento_productivo_clae = """
                                            SELECT ep.id, ep.clae2, ep.proporcion_mujeres
                                            FROM establecimiento_productivo as ep
                                            WHERE ep.clae2 IN (
                                                SELECT clae2
                                                FROM clae
                                                )
                                            ORDER BY clae2 ASC
                                           """
establecimiento_productivo = sql^limpieza_establecimiento_productivo_clae
# =============================================================================
# Vamos a quedarnos con los establecimientos productivos cuya clae sea la de productores
# orgánicos. Para eso hacemos una subquery
# =============================================================================

# =============================================================================


# =============================================================================

# Armado

# Armado dataframe de operadores orgánicos
# =============================================================================                               
armado_operadores_organicos = """
                                SELECT DISTINCT establecimiento, razón_social, departamento, id_provincia
                                FROM operadores_organicos
                                ORDER BY id_provincia ASC
                                """
df_Operadores_organicos = sql^armado_operadores_organicos      

''' Falta el segundo JOIN para tener ID_departamento '''

# =============================================================================

# Armado dataframe de producto
# =============================================================================
armado_producto = """
                 SELECT DISTINCT producto
                 FROM operadores_organicos
                 """
df_Producto = sql^armado_producto      #borarr los paréntesis 

'''QUEDA MAPEAR CON CLAE2'''
# =============================================================================

# Armado dataframe de departamento
# =============================================================================
armado_departamento = """
                         SELECT id_departamento AS id, departamento, id_provincia
                         FROM localidades                         
                        """
df_Departamento = sql^armado_departamento

# =============================================================================

# Armado dataframe de provincia
# =============================================================================
armado_provincia = """
                      SELECT DISTINCT id_provincia AS id, provincia 
                      FROM localidades
                     """
df_Provincia= sql^armado_provincia

# =============================================================================

# Armado dataframe establecimiento productivo
# =============================================================================
armado_establecimiento_productivo = """
                                    SELECT *
                                    FROM establecimiento_productivo
                                    """
df_Establecimiento_productivo = sql^armado_establecimiento_productivo
# =============================================================================

# Armado dataframe de CLAE
# =============================================================================
armado_clae = """
                SELECT *
                FROM clae
                """
df_CLAE = sql^armado_clae
 # =============================================================================

# Relaciones entre entidades

relacion_o_o_esta_depto = """
                            SELECT oo.*, id AS id_departamento
                            FROM df_Operadores_organicos AS oo
                            LEFT OUTER JOIN df_Departamento AS dep
                            ON oo.departamento = dep.departamento AND oo.id_provincia = dep.id_provincia
                            """

df_Operadores_organicos= sql^relacion_o_o_esta_depto

# Relación entre producto y operadores orgánicos 

relacion_n_m = """ 
                SELECT establecimiento, razón_social, producto
                FROM operadores_organicos
               """

df_Relacion_Produce = sql^relacion_n_m


# Ejercicio h) ii)
# =============================================================================
# ¿Cuál es el CLAE2 más frecuente en establecimientos productivos?
# Mencionar el Código y la Descripción de dicho CLAE2.
# =============================================================================
