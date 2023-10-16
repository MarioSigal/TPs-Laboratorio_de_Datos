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


# Ejercicio f)
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


limpieza_operadores_organicos = """
                                SELECT *, TRIM(UNNEST( string_to_array(productos, ','))) AS producto
                                FROM operadores_organicos
                                """
operadores_organicos = sql^limpieza_operadores_organicos


limpieza_operadores_organicos = """
                                SELECT establecimiento, razón_social, departamento, id_provincia, REPLACE(REPLACE(REPLACE(producto, '(', ''), ')', ''), '.', '') AS producto
                                FROM operadores_organicos
                                ORDER BY id_provincia ASC
                                """
operadores_organicos = sql^limpieza_operadores_organicos


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


limpieza_localidades = """
                       SELECT id_departamento, id_provincia, provincia,
                           REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(UPPER(departamento),'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U') AS departamento
                       FROM localidades
                       """
localidades = sql^limpieza_localidades


# Limpieza clae
# =============================================================================
limpieza_clae = """
                SELECT DISTINCT clae2, clae2_desc
                FROM clae
                WHERE letra = 'A' or clae2 in (10,11,13,21)
                ORDER BY clae2 ASC
              """
clae = sql^limpieza_clae


# Limpieza establecimientos productivos
# =============================================================================
limpieza_establecimiento_productivo = """
                                        SELECT ID AS id, clae2, proporcion_mujeres
                                        FROM establecimientos_productivos
                                        ORDER BY id ASC
                                    """
establecimiento_productivo = sql^limpieza_establecimiento_productivo


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

# Armado dataframe de producto
# =============================================================================
armado_producto = """
                 SELECT DISTINCT producto
                 FROM operadores_organicos
                 """
df_Producto = sql^armado_producto      #borarr los paréntesis 

# =============================================================================
# Para asignar la clae correspondiente a cada producto, como no encontramos un patrón
# ni una buena forma de hacerlo con las queries decidimos hacerlo a mano. 
# En lo personal preferimos hacerlo con pandas porque simplemente era copiar y pegar
# unas lineas de codigo lo que resultaba más rápido y menos tedioso que tener que hacerlo
# con un excel.
# =============================================================================

df_Producto['clae2'] = None

df_Producto.at[0, 'clae2'] = 21
df_Producto.at[1, 'clae2'] = 21
df_Producto.at[2, 'clae2'] = 21
df_Producto.at[3, 'clae2'] = 21
df_Producto.at[4, 'clae2'] = 21
df_Producto.at[5, 'clae2'] = 21
df_Producto.at[6, 'clae2'] = 21
df_Producto.at[7, 'clae2'] = 21
df_Producto.at[8, 'clae2'] = 21
df_Producto.at[9, 'clae2'] = 21
df_Producto.at[10, 'clae2'] = 10
df_Producto.at[11, 'clae2'] = 10
df_Producto.at[12, 'clae2'] = 1
df_Producto.at[13, 'clae2'] = 1
df_Producto.at[14, 'clae2'] = 11
df_Producto.at[15, 'clae2'] = 10
df_Producto.at[16, 'clae2'] = 1
df_Producto.at[17, 'clae2'] = 1
df_Producto.at[18, 'clae2'] = 1
df_Producto.at[19, 'clae2'] = 10
df_Producto.at[20, 'clae2'] = 1
df_Producto.at[21, 'clae2'] = 10
df_Producto.at[22, 'clae2'] = 1 
df_Producto.at[23, 'clae2'] = 10
df_Producto.at[24, 'clae2'] = 
df_Producto.at[25, 'clae2'] = 1
df_Producto.at[26, 'clae2'] = 1
df_Producto.at[27, 'clae2'] = 1
df_Producto.at[28, 'clae2'] = 1
df_Producto.at[29, 'clae2'] = 10
df_Producto.at[30, 'clae2'] = 10
df_Producto.at[31, 'clae2'] = 10
df_Producto.at[32, 'clae2'] = 10
df_Producto.at[33, 'clae2'] = 1
df_Producto.at[34, 'clae2'] = 1
df_Producto.at[35, 'clae2'] = 1
df_Producto.at[36, 'clae2'] = 1
df_Producto.at[37, 'clae2'] = 1
df_Producto.at[38, 'clae2'] = 10
df_Producto.at[39, 'clae2'] = 1
df_Producto.at[40, 'clae2'] = 1
df_Producto.at[41, 'clae2'] = 1
df_Producto.at[42, 'clae2'] = 1
df_Producto.at[43, 'clae2'] = # AGREGAR DERIVADOS TEXTILES
df_Producto.at[44, 'clae2'] = 
df_Producto.at[45, 'clae2'] = 
df_Producto.at[46, 'clae2'] =
df_Producto.at[47, 'clae2'] = 1
df_Producto.at[48, 'clae2'] = 1
df_Producto.at[49, 'clae2'] = 1
df_Producto.at[50, 'clae2'] = 10 # TRUCHAS A LAS FINAS HIERBAS
df_Producto.at[51, 'clae2'] = 10
df_Producto.at[52, 'clae2'] = 10
df_Producto.at[53, 'clae2'] = 10
df_Producto.at[54, 'clae2'] = # OTROS PRODUCTOS ORGANICOS DICE
df_Producto.at[55, 'clae2'] = 10
df_Producto.at[56, 'clae2'] = 10
df_Producto.at[57, 'clae2'] = 10
df_Producto.at[58, 'clae2'] = 10
df_Producto.at[59, 'clae2'] = 1
df_Producto.at[60, 'clae2'] = 10
df_Producto.at[61, 'clae2'] = 1
df_Producto.at[62, 'clae2'] = 10
df_Producto.at[63, 'clae2'] = 10
df_Producto.at[64, 'clae2'] = 10
df_Producto.at[65, 'clae2'] = 10
df_Producto.at[66, 'clae2'] = 10
df_Producto.at[67, 'clae2'] = 10
df_Producto.at[68, 'clae2'] = 1
df_Producto.at[69, 'clae2'] = 10
df_Producto.at[70, 'clae2'] = 10
df_Producto.at[71, 'clae2'] = 1
df_Producto.at[72, 'clae2'] = 10
df_Producto.at[73, 'clae2'] = 1
df_Producto.at[74, 'clae2'] = 10
df_Producto.at[75, 'clae2'] = 10
df_Producto.at[76, 'clae2'] = 1
df_Producto.at[77, 'clae2'] = 10
df_Producto.at[78, 'clae2'] = 1
df_Producto.at[79, 'clae2'] = 1
df_Producto.at[80, 'clae2'] = 10
df_Producto.at[81, 'clae2'] = 10
df_Producto.at[82, 'clae2'] = 10
df_Producto.at[83, 'clae2'] = 10
df_Producto.at[84, 'clae2'] = 10
df_Producto.at[85, 'clae2'] = 10
df_Producto.at[86, 'clae2'] = 1
df_Producto.at[87, 'clae2'] = 1
df_Producto.at[88, 'clae2'] = 1
df_Producto.at[89, 'clae2'] = 10
df_Producto.at[90, 'clae2'] = 1
df_Producto.at[91, 'clae2'] = 1
df_Producto.at[92, 'clae2'] = 10
df_Producto.at[93, 'clae2'] = 10
df_Producto.at[94, 'clae2'] = 10
df_Producto.at[95, 'clae2'] = 10
df_Producto.at[96, 'clae2'] = 1
df_Producto.at[97, 'clae2'] = 10
df_Producto.at[98, 'clae2'] = 1
df_Producto.at[99, 'clae2'] = 21 ''' CHECKEAR '''
df_Producto.at[100, 'clae2'] = 1
df_Producto.at[101, 'clae2'] = 1
df_Producto.at[102, 'clae2'] =  
df_Producto.at[103, 'clae2'] = 10
df_Producto.at[104, 'clae2'] = 10
df_Producto.at[105, 'clae2'] = 10
df_Producto.at[106, 'clae2'] = 
df_Producto.at[107, 'clae2'] = 
df_Producto.at[108, 'clae2'] = 1
df_Producto.at[109, 'clae2'] = 1
df_Producto.at[110, 'clae2'] = 1 '''CHECKEAR'''
df_Producto.at[111, 'clae2'] = ''' HABRIA QUE ELIMINAR '''
df_Producto.at[112, 'clae2'] = 1
df_Producto.at[113, 'clae2'] = 1
df_Producto.at[114, 'clae2'] = 1
df_Producto.at[115, 'clae2'] = 1
df_Producto.at[116, 'clae2'] = 1
df_Producto.at[117, 'clae2'] = 
df_Producto.at[118, 'clae2'] = 1
df_Producto.at[119, 'clae2'] = 1
df_Producto.at[120, 'clae2'] = 1
df_Producto.at[121, 'clae2'] = 1
df_Producto.at[122, 'clae2'] = 1
df_Producto.at[123, 'clae2'] = 1
df_Producto.at[124, 'clae2'] = 1
df_Producto.at[125, 'clae2'] = 1
df_Producto.at[126, 'clae2'] = 1
df_Producto.at[127, 'clae2'] = 1
df_Producto.at[128, 'clae2'] = 1
df_Producto.at[129, 'clae2'] = 1
df_Producto.at[130, 'clae2'] = 1
df_Producto.at[131, 'clae2'] = 1
df_Producto.at[132, 'clae2'] = 1
df_Producto.at[133, 'clae2'] = 1
df_Producto.at[134, 'clae2'] = 1
df_Producto.at[135, 'clae2'] = 1
df_Producto.at[136, 'clae2'] = 1
df_Producto.at[137, 'clae2'] = 1
df_Producto.at[138, 'clae2'] = 2 ''' CHECKEAR '''
df_Producto.at[139, 'clae2'] = 1
df_Producto.at[140, 'clae2'] = 1
df_Producto.at[141, 'clae2'] = 1 # ESTO NO IRIA PERO BUENO
df_Producto.at[142, 'clae2'] = 1 # WTF
df_Producto.at[143, 'clae2'] = 1 # MUY DECLARATIVO
df_Producto.at[144, 'clae2'] = 1
df_Producto.at[145, 'clae2'] = 1
df_Producto.at[146, 'clae2'] = 1
df_Producto.at[147, 'clae2'] = 
df_Producto.at[148, 'clae2'] = 1
df_Producto.at[149, 'clae2'] = 1
df_Producto.at[150, 'clae2'] = 1
df_Producto.at[151, 'clae2'] = 1
df_Producto.at[152, 'clae2'] = 2 '''CHECKEAR'''
df_Producto.at[153, 'clae2'] = 1
df_Producto.at[154, 'clae2'] = 1
df_Producto.at[155, 'clae2'] = 1
df_Producto.at[156, 'clae2'] = ''' PARA MI ES 10 PERO DESPUÉS SE VE'''
df_Producto.at[157, 'clae2'] = 1 ''' CHECKEAR '''
df_Producto.at[158, 'clae2'] = 1
df_Producto.at[159, 'clae2'] = 1
df_Producto.at[160, 'clae2'] = 1
df_Producto.at[161, 'clae2'] = 1
df_Producto.at[162, 'clae2'] = 1
df_Producto.at[163, 'clae2'] = 1
df_Producto.at[164, 'clae2'] = 1
df_Producto.at[165, 'clae2'] = 1
df_Producto.at[166, 'clae2'] = 1
df_Producto.at[167, 'clae2'] = 1
df_Producto.at[168, 'clae2'] = 1
df_Producto.at[169, 'clae2'] = 1
df_Producto.at[170, 'clae2'] = 1
df_Producto.at[171, 'clae2'] = 1
df_Producto.at[172, 'clae2'] = 1
df_Producto.at[173, 'clae2'] = 1
df_Producto.at[174, 'clae2'] = 1
df_Producto.at[175, 'clae2'] = 1
df_Producto.at[176, 'clae2'] = 
df_Producto.at[177, 'clae2'] = 1
df_Producto.at[178, 'clae2'] = 1
df_Producto.at[179, 'clae2'] = 1
df_Producto.at[180, 'clae2'] = 1
df_Producto.at[181, 'clae2'] = 
df_Producto.at[182, 'clae2'] = 1
df_Producto.at[183, 'clae2'] = 1
df_Producto.at[184, 'clae2'] = 1
df_Producto.at[185, 'clae2'] = 1
df_Producto.at[186, 'clae2'] = 1
df_Producto.at[187, 'clae2'] = 
df_Producto.at[188, 'clae2'] = 1
df_Producto.at[189, 'clae2'] = 1
df_Producto.at[190, 'clae2'] = 1
df_Producto.at[191, 'clae2'] = 1
df_Producto.at[192, 'clae2'] = 1
df_Producto.at[193, 'clae2'] = 1
df_Producto.at[194, 'clae2'] = 1
df_Producto.at[195, 'clae2'] = 1
df_Producto.at[196, 'clae2'] = 
df_Producto.at[197, 'clae2'] = 1
df_Producto.at[198, 'clae2'] = 1
df_Producto.at[199, 'clae2'] = 1
df_Producto.at[200, 'clae2'] = 1
df_Producto.at[201, 'clae2'] = 21 '''CHECKEAR'''
df_Producto.at[202, 'clae2'] = 21
df_Producto.at[203, 'clae2'] = 1
df_Producto.at[204, 'clae2'] = 1
df_Producto.at[205, 'clae2'] = 1 '''DICE REMNOLACHA CORREGIR'''
df_Producto.at[206, 'clae2'] = 1 ''' ES LA MISMA PLANTA QUE EL bok choy'''
df_Producto.at[207, 'clae2'] = 1
df_Producto.at[208, 'clae2'] = 1
df_Producto.at[209, 'clae2'] = 1
df_Producto.at[210, 'clae2'] = 1
df_Producto.at[211, 'clae2'] = 1







df_Producto.at[590, 'clae2'] = 10
df_Producto.at[591, 'clae2'] = 10 '''Checkear'''
df_Producto.at[592, 'clae2'] = 1
df_Producto.at[593, 'clae2'] = 1 '''Checkear'''
df_Producto.at[594, 'clae2'] = 1 '''Checkear '''
df_Producto.at[595, 'clae2'] = 11 ''' Checkear'''
df_Producto.at[596, 'clae2'] = 
df_Producto.at[597, 'clae2'] = 21
df_Producto.at[598, 'clae2'] = 

'''QUEDA MAPEAR CON CLAE2'''
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
