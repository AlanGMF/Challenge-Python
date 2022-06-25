from sqlalchemy import  create_engine
from sqlalchemy import text
from configs import *
import logging
import sys

logging.basicConfig(
    filename='logs.log',
    level=logging.INFO,
    format='%(asctime)s,%(filename)s,%(levelname)s,%(message)s')

if __name__=='__main__':

    try:    
        engine = create_engine(CONN_DB, echo=False)
        logging.info("Coneccion con Base de Datos exitosa")

        for ruta in RUTAS:
            sentencia_sql = open(ruta,"r")
            consulta = text(sentencia_sql.read())
            engine.execute(consulta)

        logging.info("Se crearon las tablas en la Base de Datos")
        
    except:
        logging.critical("No se pudo conectar a la base de datos")
        sys.exit()
