#importamos librerias 
import numpy as np 
import pandas as pd 
import ast
import fastapi as FastAPI

app = FastAPI.FastAPI()
#importamos la data 
data = pd.read_csv("mi_movies_dataset.csv")

#Los valores nulos de los campos revenue, budget deben ser rellenados por el número 0.
data["revenue"].fillna(0, inplace = True)
data["budget"].fillna(0, inplace = True)
#convierto los valores de la columna budhet en valores flotantes para poder realizar la duvision ya que estaban como objetos
data['budget'] = data['budget'].astype(float)

def calcular_retorno(row):
    revenue = row['revenue']
    budget = row['budget']
    
    if pd.notnull(revenue) and pd.notnull(budget) and budget != 0:
        return revenue / budget
    else:
        return 0

# Crear la columna 'return' aplicando la función calcular_retorno a cada fila
data['return'] = data.apply(calcular_retorno, axis=1)

import fastapi as FastAPI

app = FastAPI.FastAPI()

@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes: str): 
     '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron 
        ese mes 
    '''
     #nos imprimira el ideoma que le indiquemos  
     meses_espanol_ingles = {
     'enero': 'January',
     'febrero': 'February',
     'marzo': 'March',
     'abril': 'April',
     'mayo': 'May',
     'junio': 'June',
     'julio': 'July',
     'agosto': 'August',
     'septiembre': 'September',
     'octubre': 'October',
     'noviembre': 'November',
     'diciembre': 'December'}
   
     if mes.lower() in meses_espanol_ingles:
        mes_mediador = meses_espanol_ingles[mes.lower()]
     elif mes.lower not in meses_espanol_ingles:
        mes_mediador = mes
        
    #Convertimos a la columna de tipo datetime
     data["release_date"] = pd.to_datetime(data["release_date"])
    
    #Obtenemos mes y año de la columna
     data['mes'] = data['release_date'].dt.month_name() 
     data['año'] = data['release_date'].dt.year

    #Filtramos por el mes proporcionado
     peliculas_mes = data[data['mes'].str.lower() == mes_mediador.lower()]
    
    #Cantidada de pelicula por mes 
     cantidad = len(peliculas_mes)
    
     return {'mes':mes, 'cantidad':cantidad}


@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia:str):
    '''
    Se ingresa el dia y la funcion retorna la cantidad de peliculas que se 
    estrenaron ese dia 

    ''' 
    #imprimira el ideoma que le indiquemos 
    dias_espanol_ingles = {
    'lunes': 'Monday',
    'martes': 'Tuesday',
    'miércoles': 'Wednesday',
    'jueves': 'Thursday',
    'viernes': 'Friday',
    'sábado': 'Saturday',
    'domingo': 'Sunday'}
    
    if dia.lower() in dias_espanol_ingles:
        dia_mediador = dias_espanol_ingles[dia.lower()]
    elif dia.lower not in dias_espanol_ingles:
        dia_mediador = dia
        
    # Convertir la columna a tipo datetime 
    data['release_date'] = pd.to_datetime(data['release_date']) 

    # Obtener el día de la semana de la columna
    data['dia_semana'] = data['release_date'].dt.day_name()

    # Filtrar  por el día de la semana proporcionado
    peliculas_dia = data[data['dia_semana'].str.lower() == dia_mediador.lower()]
 
    cantidad = len(peliculas_dia) 
    return  {'dia': dia, 'cantidad': cantidad}


@app.get("/franquicia/{franquicia}")
def franquicia(franquicia): 
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y 
    promedio
    ''' 
    # Filtrar  por la franquicia proporcionada
    franquicia_data = data[data['belongs_to_collection'].notnull() & data['belongs_to_collection'].apply(lambda x: isinstance(x, str) and franquicia.lower() in x.lower())]

    # Obtener la cantidad de películas en la franquicia
    cantidad = len(franquicia_data)

    # Calcular la ganancia total y el promedio de la franquicia
    ganancia_total = franquicia_data['revenue'].sum()
    ganancia_promedio = franquicia_data['revenue'].mean()

    
    return {'franquicia':franquicia, 'cantidad': cantidad, 'ganancia_total':ganancia_total, 'ganancia_promedio':ganancia_promedio}

@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais: str):
    
    # Filtrar la data por el país proporcionado
    pelicula_pais = data[data["production_countries"].str.contains(pais, case=False, na=False)]


    # cantidad de películas producidas en el país
    cantidad = len(pelicula_pais)

    return {'pais': pais, 'cantidad': cantidad}


@app.get("/productora/{productora}")
def productoras(productora:str):
    ''' 
    Ingresas la productora, retornando la ganancia total y la cantidad de peliculas que produjero
    ''' 
     # Filtrar por la productora proporcionada
    produ = data[["production_companies", "budget", "revenue"]].dropna()
    produ["production_companies"] = produ["production_companies"].map(str.lower)

    # Obtener la ganancia total y la cantidad de películas producidas por la productora
    cantidad = produ.shape[0]
    ganacia_total = (produ["revenue"]- produ["budget"]).sum()

    return {"productora": productora, "ganancia total": ganacia_total, "cantidad": cantidad}


@app.get("/retorno/{pelicula}")
def retorno(pelicula: str): 
    '''Ingresas la pelicula, retornando la inversion, la ganancia, 
    el retorno y el año en el que se lanzo
    ''' 
    #filtramos las filas correspondientes 
    fila_pelicula = data[data["title"] == pelicula].iloc[0]
    
    #sacamos los valores 
    inversion = float(fila_pelicula["budget"])
    ganancia = float(fila_pelicula["revenue"]) - inversion
    retorno = float(fila_pelicula["return"])
    anio = int(fila_pelicula["release_year"])

    return {'pelicula':pelicula, 'inversion':inversion, 'ganacia':ganancia,'retorno': retorno, 'anio': anio}
