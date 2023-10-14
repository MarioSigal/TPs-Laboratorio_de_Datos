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

df_Operadores_organicos = pd.DataFrame(columns=['establecimiento', 'razón_social', 'departamento', 'id_departamento'])
df_Producto = pd.DataFrame(columns=['producto', 'clae3']) 
df_Departamento = pd.DataFrame(columns=['id', 'departamento', 'id_provincia'])
df_Provincia = pd.DataFrame(columns=['id', 'provincia'])
df_Establecimiento_productivo = pd.DataFrame(columns=['id', 'clae2', 'proporción_mujeres'])
df_CLAE = pd.DataFrame(columns=['clae3','clae3_desc', 'clae2', 'clae2_desc'])
# relación entre operadores orgánicos y producto
df_Relacion_Produce = pd.DataFrame(columns=['establecimiento', 'razón_social', 'producto'])


# Ejercicio h) i)

# Limpieza

limpieza_operadores_organicos = """
                                SELECT REGEXP_REPLACE(establecimiento, '\\bNC\\b', 'ESTABLECIMIENTO ÚNICO') AS establecimiento, 'razón social' AS razón_social,
                                    departamento, REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(productos,':',','), ' Y ',', '),'+',','),'-',','),'?',',') AS productos
                                FROM operadores_organicos;
                                """
operadores_organicos = sql^limpieza_operadores_organicos


limpieza_operadores_organicos = """
                                SELECT *, TRIM(UNNEST( string_to_array(productos, ','))) AS producto
                                FROM operadores_organicos
                                """
operadores_organicos = sql^limpieza_operadores_organicos


limpieza_operadores_organicos = """
                                SELECT establecimiento, razón_social, departamento, REPLACE(REPLACE(REPLACE(producto, '(', ''), ')', ''), '.', '') AS producto
                                FROM operadores_organicos
                                """
operadores_organicos = sql^limpieza_operadores_organicos


limpieza_localidades = """
                        SELECT DISTINCT REPLACE(codigo_indec_departamento,'02001,02002,02003,02004,02005,02006,02007,02008,02009,02010,02011,02012,02013,02014,02015', '02001') AS id_departamento,
                            REPLACE(nombre_departamento,'Comuna 1,Comuna 10,Comuna 11,Comuna 12,Comuna 13,Comuna 14,Comuna 15,Comuna 2,Comuna 3,Comuna 4,Comuna 5,Comuna 6,Comuna 7,Comuna 8,Comuna 9', 'CIUDAD AUTONOMA BUENOS AIRES') AS departamento,
                            codigo_indec_provincia AS id_provincia, nombre_provincia AS provincia
                        FROM localidades                         
                        ORDER BY id_provincia ASC, id_departamento ASC
                        """
localidades = sql^limpieza_localidades   # Nos aparecieron todas las comunas de CABA juntas por lo que vamos a renombrar a las comunas como CABA y su índice será el mayor de los que aparecía


limpieza_localidades = """
                       SELECT id_departamento, id_provincia, provincia,
                       REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(UPPER(departamento),'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U') AS departamento
                       FROM localidades
                       """
localidades = sql^limpieza_localidades


limpieza_establecimiento_productivo = """
                                        SELECT ID AS id, clae2, proporcion_mujeres
                                        FROM establecimientos_productivos
                                        ORDER BY id ASC
                                    """
establecimiento_productivo = sql^limpieza_establecimiento_productivo


limpieza_clae = """
                SELECT DISTINCT clae3, clae3_desc, clae2, clae2_desc
                FROM clae
                WHERE letra = 'A' or (letra = 'C' and (clae2 = 10 or clae2 = 11))
                ORDER BY clae2 ASC, clae3 ASC
              """
clae = sql^limpieza_clae


# Armado
                               
armado_operadores_organicos = """
                                SELECT DISTINCT establecimiento, razón_social, departamento
                                FROM operadores_organicos
                                """
df_Operadores_organicos = sql^armado_operadores_organicos      


armado_producto = """
                 SELECT DISTINCT producto
                 FROM operadores_organicos
                 """
df_Producto = sql^armado_producto      #borarr los paréntesis 


armado_departamento = """
                         SELECT id_departamento AS id, departamento, id_provincia
                         FROM localidades                         
                        """
df_Departamento = sql^armado_departamento


armado_provincia = """
                      SELECT DISTINCT id_provincia AS id, provincia 
                      FROM localidades
                     """
df_Provincia= sql^armado_provincia


armado_establecimiento_productivo = """
                                    SELECT *
                                    FROM establecimiento_productivo
                                    """
df_Establecimiento_productivo = sql^armado_establecimiento_productivo


armado_clae = """
                SELECT *
                FROM clae
                """
df_CLAE = sql^armado_clae
 

# Relaciones entre entidades


# Ejercicio h) ii)
# =============================================================================
# ¿Cuál es el CLAE2 más frecuente en establecimientos productivos?
# Mencionar el Código y la Descripción de dicho CLAE2.
# =============================================================================

