import pandas as pd
import numpy as np
import validators

def tel_valido(tel):
    """
    valida si lo que recibe es una cadena string numerica o un int,
    y devuelve np.nan en caso de no recibir un string o no ser un int
    """
    if type(tel) == str:
        tel.replace(" ","")
        if tel.isnumeric():
            return tel
    elif type(tel) == int:
        return 
    return np.nan

def validacion_cp(cp):
    """
    valida si lo que recibe es una cadena string alfanumerica o numerica
    y devuelve np.nan en caso de no recibir un string
    """
    if type(cp) == str:
        if cp.isnumeric() or cp.isalnum():
            return cp
    return np.nan

def web_o_nan(d):
    """
    al recivir un str se le agrega ( http:// ) de no tenerlo.
    se devuelve np.nan en caso de no ser una pagina valida
    """
    principio_pagina="http://"
    principio_pagina_s="https://"
    if type(d) == str:
        
        if d.find(principio_pagina_s) >=0 or d.find(principio_pagina) >= 0:
            es_una_web_valida = validators.url(d)
        else:
            d=principio_pagina+d
            es_una_web_valida = validators.url(d)
            
        if type(es_una_web_valida) == bool and es_una_web_valida:
            return d
        else: 
            return np.nan
    else:
        return np.nan

def mail_o_nan(mail):
    """valida si recibe un string y es un email
        devolviendo np.nan en caso de contrario
    """
    if type(mail) == str and validators.email(mail) == True:
        return mail
    return np.nan


def int_o_cero(numero):
    """valida si recibe un entero
        devolviendo 0 en caso de contrario
    """
    if type(numero) != int:
        return 0
    return numero

def string_o_nan(palabra):
    """valida si recibe un string no numerico 
        devolviendo np.nan en caso de contrario
    """
    if type(palabra) != str:
        return np.nan
    if palabra.isnumeric() or palabra.isspace() or palabra=="":
        return np.nan
    return palabra

def incaa_o_false(valor):
    """valida si recibe "si" de tipo string retornando 1 en su lugar
        y devolviendo un booleano: False en caso de contrario
    """
    if type(valor) == str and valor.lower() == "si":
        return 1
    elif type(valor) == int and valor == 1:
        return 1
    return False
