

import pandas
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

import sys
import logging
import datetime

from configs import *
from validaciones import *
from recolector import extraer

logging.basicConfig(
    filename='logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

dfs = []
dic_categ_ruta = {}

ajustes_columnas = {
    'telefono':'número de teléfono',
    'teléfono':'número de teléfono',
    'categoria':'categoría',
    'cod_loc':'cod_localidad',
    'dirección':'domicilio',
    'direccion':'domicilio',
    'cp':'código postal'
}

provincias_id = {
    "Jujuy":"1",
    "Salta":"2",
    "Formosa":"3",
    "Misiones":"4",
    "Chaco":"5",
    "Corrientes":"6",
    "Tucumán":"7",
    "Santiago del Estero":"8",
    "Catamarca":"9",
    "Santa Fe":"10",
    "La Rioja":"11",
    "San Juan":"12",
    "Entre Ríos":"13",
    "Córdoba":"14",
    "San Luis":"15",
    "Mendoza":"16",
    "La Pampa":"17",
    "Buenos Aires":"18",
    "Ciudad Autónoma de Buenos Aires":"19",
    "Neuquén":"20",
    "Río Negro":"21",
    "Chubut":"22",
    "Santa Cruz":"23",
    "Tierra del Fuego, Antártida e Islas del Atlántico Sur":"24",
    
}

tabla_concat_columnas = [
    'cod_localidad',
    'idprovincia',
    'iddepartamento',
    'categoría',
    'provincia',
    'localidad',
    'nombre',
    'domicilio',
    'código postal',
    'número de teléfono',
    'mail',
    'web'
]

if __name__ == '__main__':

    logging.info("--- Empieza a correr el programa ---")

    #se verifica la conneccion a la Base de Datos
    try:
        engine = create_engine(
                BD,echo=False
            )
        engine.connect()
        logging.info("Coneccion con Base de Datos exitosa")
    except SQLAlchemyError as err:
        logging.critical(f"No se pudo conectar a la base de datos {err}")
        sys.exit()

    #se verifica existencia de tablas en la BD
    insp = sqlalchemy.inspect(engine)
    t1 = insp.has_table("tabla_cine", schema="public")
    t2 = insp.has_table("tabla_concat", schema="public")

    if t1 and t2:
        logging.info("Se encontraron las tablas en la base de datos")
    else:
        logging.critical("No se encontraron las tablas en la base de datos")
        sys.exit()
    

    # EXTRACCION de archivos fuente

    #se extraen las urls y se guardan las rutas en un dict
    for categoria, url in DICCIONARIO.items():

        ruta = extraer(categoria,url)
        dic_categ_ruta[categoria] = ruta
    logging.info("Termina extraccion de archivos")   

    # PROCESAMIENTO de datos
    for categoria,ruta in dic_categ_ruta.items():
        
        #se lee el archivo csv
        df = pandas.read_csv(ruta, encoding='utf-8')

        #transforma minusculas las indice columnas
        colums_df = df.columns
        columnas_en_minuscul = []

        for columna in colums_df:
            columnas_en_minuscul.append(columna.lower())

        df.columns = columnas_en_minuscul

        #se ajusta los nombres de columnas
        df.rename(columns = ajustes_columnas, inplace = True)

        #se corrijen nombres de provincias
        df.loc[df.provincia == 'Santa Fé'] = 'Santa Fe'
        df.loc[df.provincia == "Neuquén\xa0"] = "Neuquén"
        
        df['mail'] = df['mail'].apply(mail_o_nan)
        df['código postal'] = df['código postal'].apply(validacion_cp)
        df['web'] = df['web'].apply(web_o_nan)
        df['número de teléfono'] = df['número de teléfono'].apply(tel_valido)

        df['cod_localidad'] = df['cod_localidad'].apply(int_o_cero)
        df.loc[df.cod_localidad == 0, :] = np.nan
        df['idprovincia'] = df['idprovincia'].apply(int_o_cero)
        df.loc[df.idprovincia == 0, :] = np.nan
        df['iddepartamento'] = df['iddepartamento'].apply(int_o_cero)
        df.loc[df.iddepartamento == 0, :] = np.nan

        df['categoría'] = df['categoría'].apply(string_o_nan)
        df['localidad'] = df['localidad'].apply(string_o_nan)

        df['nombre'] = df['nombre'].apply(string_o_nan)

        if "espacio_incaa" in df.columns:
            df['espacio_incaa'] = df['espacio_incaa'].apply(incaa_o_false)
            df_cine = df

        dfs.append(df)
        logging.info(f"se procesa {categoria} correctamente")

    #formo la primera tabla
    df_total = pandas.concat(dfs,axis=0)

    #unifico idprovincia para no tener ids distintas
    for provincia,id in provincias_id.items():   
        df_total.loc[df_total.provincia == provincia, 'idprovincia'] = id

    #se filtran las columnas y se agrega columna fecha
    df_total = df_total.loc[:,tabla_concat_columnas]
    df_total['fecha de carga'] = datetime.datetime.now().strftime("%d/%m/%y")
    prov ='Tierra del Fuego, Antártida e Islas del Atlántico Sur'
    df.loc[df.provincia == 'Tierra del Fuego'] = prov
    #formo la segunda tabla
    df_cine = df_cine.groupby(['provincia'],as_index = False)[
        'pantallas','butacas','espacio_incaa'].sum()

    df_cine['fecha de carga'] = datetime.datetime.now().strftime("%d/%m/%y")

    logging.info("Termina el prosesamiento de datos")

    #ACTUALIZACION de la base de datos
    try:
        df_total.to_sql(name= "tabla_concat",
                        con= engine, index= False,
                        if_exists= "replace")

        df_cine.to_sql(name= "tabla_cine",
                        con= engine, index= False,
                        if_exists= "replace")

        logging.info("Se actualizo correctamente la Base de Datos")
    except:
        logging.error(
            "No se pudo actualizar los datos en las tablas de la Base de Datos"
            )

    logging.info("--- Termina programa ---")