from pathlib import Path
from decouple import config


#rutas sql
RUTA_T1=Path.cwd() / 'sql' / "tabla_concat.sql"
RUTA_T2=Path.cwd() / 'sql' / "tabla_cine.sql"

#urls
MUSEO="https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d"
CINE="https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_392ce1a8-ef11-4776-b280-6f1c7fae16ae" 
BIBLIOTECA="https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7"

BD = config('CONN_DB')

#nombre archivos
N_1 = "museo"
N_2 = "cine"
N_3 = "biblioteca"

DICCIONARIO={
    N_1 : MUSEO,
    N_2 : CINE,
    N_3 : BIBLIOTECA
}