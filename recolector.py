import requests
from requests import ConnectionError
from bs4 import BeautifulSoup

import os
from pathlib  import Path

import pandas
import datetime
import logging
import sys

mes_esp={
        1:"enero",
        2:"febrero",
        3:"marzo",
        4:"abril",
        5:"mayo",
        6:"junio",
        7:"julio",
        8:"agosto",
        9:"septiembre",
        10:"octubre",
        11:"noviembre",
        12:"diciembre"
    }

fecha=datetime.datetime.now()
mes = mes_esp[fecha.month]
anio = str(fecha.year)

def extraer(categoria: str, url: str ):
    """
    recive un nombre y una direccion url de tipo string
    devuelve una ruta tipo Path en la cual guarda el archivo csv
    con el nombre dado.
    """
    
    #desde la url se scrapea el link que brinda un archivo csv
    try:
        pagina = requests.get(url)
        soup = BeautifulSoup(pagina.text,"html.parser")
    except(ConnectionError, Exception):
        logging.critical(f"No se pudo acceder a {url}")
        sys.exit()
    try:
        link_csv = soup.find('a',class_='btn btn-green btn-block').get('href')
        logging.info(f"Link de csv obtenido: {link_csv[:30]}...{link_csv[-20:]}") #corregir LOG
    except:
        logging.critical("BeautifulSoup no pudo encontrar el link necesario para extraer el csv")
        sys.exit()

    #se extrae el csv del link
    try:
        #agrego user-agent para evitar error 403 forbidden que tira el servidor
        storage_options = {'User-Agent': 'Mozilla/5.0'}
        #se lee el csv con pandas
        df=pandas.read_csv(link_csv,storage_options=storage_options)
    except:
        logging.critical(f"No se pudo obtener archivo desde: {link_csv}")
        sys.exit()
    
    else:
        #crea carpetas
        Path.joinpath(Path.cwd(), categoria, anio+ "-"+ mes).mkdir(parents = True,exist_ok = True)
        carpeta_creada = Path.joinpath(Path.cwd(),categoria,str(str(fecha.year)+"-"+mes))
        logging.info(f"se crean carpetas para archivo {categoria}")

        #se forma el nombre del archivo csv
        nombre_archivo = categoria+"-"+fecha.strftime("%d-%m-%y")+".csv"
        carpeta_actual=Path.cwd()

        #se guarda el csv
        os.chdir(carpeta_creada)
        df.to_csv(nombre_archivo)
        os.chdir(carpeta_actual)
        logging.info(f"se guardo archivo {categoria} correctamente")
        
        return carpeta_creada.joinpath(nombre_archivo)

