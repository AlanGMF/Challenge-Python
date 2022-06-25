from sqlalchemy import  create_engine
from sqlalchemy import text
from configuracion import *

if __name__=='__main__':

    try:    
        engine = create_engine(
            BD,echo=False
        )
        print("CONECCION EXITOSA*******************")

        primera_tabla=open(RUTA_T1,"r")
        tabla_cine=open(RUTA_T2,"r")
        query=text(primera_tabla.read())
        query2=text(tabla_cine.read())
        engine.execute(query)
        print("se creo PRIMERAtabla *******************")
        engine.execute(query2)
        print("se creo SEGUNDA tabla *******************")
    except:
        print("no se tener acceso a la bd")