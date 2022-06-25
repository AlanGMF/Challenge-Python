# Challenge-Python
Challenge Data Analytics y Python

## Clonar repositorio
```
git clone https://github.com/AlanGMF/Challenge-Python
```
## :wrench: Crear y activar entorno virtual (venv)
- Windows
```
py -m venv venv
```
```
.\venv\Scripts\activate
```
- Mac/Linux
```
python3 -m venv venv
```
```
source venv/bin/activate
```
## ⚙️ Instalar dependencias
```
pip install -r requirements.txt
```

## :file_folder: Conectar a la Base de Datos PostgreSQL

Crear un archivo .env en el directorio del proyecto y agregar los siguientes campos con sus respectivos valores:
```
User_ID = root
Password = myPassword
Host = localhost
Port = 5432
Database = myDataBase
```
## ⚡️ Correr el programa
- Windows

  Crear las tablas en la base de datos
  ```
  py scripts.py
  ```
  Extraer procesar y actualizar la base de datos
  ```
  py main.py
  ```
- Mac/Linux

  Crear las tablas en la base de datos
  ```
  python3 scripts.py
  ```
  Extraer procesar y actualizar la base de datos
  ```
  python3 main.py
  ```
