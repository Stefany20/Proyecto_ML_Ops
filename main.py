#importamos librerias 
import numpy as np 
import pandas as pd 
import ast
import fastapi as FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


app = FastAPI.FastAPI()
#importamos la data 
data = pd.read_csv("restaurado_movies_dataset.csv")

#Los valores nulos de los campos revenue, budget deben ser rellenados por el número 0.
data["revenue"].fillna(0, inplace = True)
data["budget"].fillna(0, inplace = True)
#convierto los valores de la columna budhet en valores flotantes para poder realizar la duvision ya que estaban como objetos
data['budget'] = data['budget'].astype(float)

def calcular_retor(row):
    revenue = row['revenue']
    budget = row['budget']
    
    if pd.notnull(revenue) and pd.notnull(budget) and budget != 0:
        return revenue / budget
    else:
        return 0

# Crear la columna 'return' aplicando la función calcular_retorno a cada fila
data['return'] = data.apply(calcular_retor, axis=1)



@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes: str): 
    '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron 
        ese mes 
    ''' 
#nos imprimira el ideoma que le indiquemos  
    espanol_ingles = {
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
   
    if mes.lower() in espanol_ingles:
        mes_medi = espanol_ingles[mes.lower()]
    elif mes.lower not in espanol_ingles:
        mes_medi = mes
        
    #Convertimos a la columna de tipo datetime
    data["release_date"] = pd.to_datetime(data["release_date"])
    
    #Obtenemos mes y año de la columna
    data['mes'] = data['release_date'].dt.month_name() 
    data['año'] = data['release_date'].dt.year

    #Filtramos por el mes proporcionado
    peliculas_mes = data[data['mes'].str.lower() == mes_medi.lower()]
    
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
    espanol_ingles = {
    'lunes': 'Monday',
    'martes': 'Tuesday',
    'miércoles': 'Wednesday',
    'jueves': 'Thursday',
    'viernes': 'Friday',
    'sábado': 'Saturday',
    'domingo': 'Sunday'}
    
    if dia.lower() in espanol_ingles:
        dia_medi = espanol_ingles[dia.lower()]
    elif dia.lower not in espanol_ingles:
        dia_medi = dia
        
    # Convertir la columna a tipo datetime 
    data['release_date'] = pd.to_datetime(data['release_date']) 

    # Obtener el día de la semana de la columna
    data['dia_semana'] = data['release_date'].dt.day_name()

    # Filtrar  por el día de la semana proporcionado
    peliculas_dia = data[data['dia_semana'].str.lower() == dia_medi.lower()]
 
    cantidad = len(peliculas_dia) 
    return  {'dia': dia, 'cantidad': cantidad}


@app.get("/franquicia/{franquicia}")
def franquicia(franquicia: str):
    '''
    Se ingresa la franquicia, retornando la
      cantidad de peliculas, ganancia total y promedio
    '''
    # Filtro el DataFrame por la franquicia proporcionada
    franquicia_fi = data[data['belongs_to_collection'].notnull() & data['belongs_to_collection'].apply(lambda x: isinstance(x, str) and franquicia.lower() in x.lower())]

    cantidad = len(franquicia_fi)

    ganancia_en_total = franquicia_fi['revenue'].sum()-franquicia_fi['budget'].sum()
    ganancia_en_promedio = ganancia_en_total/cantidad

    return {'franquicia': franquicia, 'cantidad': cantidad, 'ganancia_total': ganancia_en_total, 'ganancia_promedio': ganancia_en_promedio}

@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais: str):
    '''
    Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo
    '''
    # Filtrar la data por el país proporcionado
    pelicula_pais = data[data["production_countries"].str.contains(pais, case=False, na=False)]


    # cantidad de películas producidas en el país
    cantidad = len(pelicula_pais)

    return {'pais': pais, 'cantidad': cantidad}


@app.get("/retorno/{productora}")
def productoras(productora: str):
    '''
    Ingresas la productora, retornando la ganancia total y 
    la cantidad de peliculas que produjeron
    '''
    # Filtro por la productora proporcionada
    productora_fil = data[data['production_companies'].notnull() & data['production_companies'].str.contains(productora, case=False)]

    # Obtener la ganancia total y la cantidad de películas producidas por la productora
    ganancia_en_total = productora_fil['revenue'].sum()-productora_fil['budget'].sum()
    cantidad = len(productora_fil)

    return {'productora': productora, 'ganancia_total': ganancia_en_total, 'cantidad': cantidad}


@app.get("/recomendaciones/{recomendacion}")
def recomendaciones(titulo : str):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['title'])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    indice = data[data['title'] == titulo].index[0]
    puntuaciones_similares = list(enumerate(cosine_similarities[indice]))
    puntuaciones_similares = sorted(puntuaciones_similares, key=lambda x: x[1], reverse=True)
    puntuaciones_similares = puntuaciones_similares[1:6]  # Obtiene las 5 películas más similares
    
    indices_peliculas = [i[0] for i in puntuaciones_similares]
    
    recomendacion = {'lista recomendada': [data['title'].iloc[i] for i in indices_peliculas]}
    return recomendacion