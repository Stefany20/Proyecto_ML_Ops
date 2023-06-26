<p align=right><img src=https://th.bing.com/th/id/OIP.CUqEPGqSzaHYWS3lfwSqJwHaHa? height=40>><p>

# <h1 align=center> **PROYECTO INDIVIDUAL # 1**</h1>

## **Machine Learning Operations ** 
### *Por Rojas Perez, Stefany (DS-10)*


## ESTRUCTURA DEL PROYECTO** :white_circle:

A continuación podrá visualizarse el proyecto finalizado con su estructura de archivos y carpetas

Los principales archivos desarrollados (que en el apartado siguiente se describirán en forma detallada y precisa su contenido, son:
- Transformacion - Funciones
- EDA - Recomendacion
- main.py

## SOLUCIÓN DEL PROYECTO :white_circle:

### 1. Etapa del proceso ETL :

Archivo principal: **[Transformacion - Funciones](Preparacion de Datos.ipynb)**
- Se realizó el proceso de ETL (extracción, transformación y carga).

- Los valores nulos de los campos revenue, budget se rellenaron con el número 0.

- Fechas  la pasamos a formato AAAA-mm-dd, creamos una columna  release_year donde extraemos el año de la fecha de estreno.

-Crearmos la columna con el retorno de inversión, llamada return con los campos revenue y budget, 
dividiendo estas dos últimas revenue / budget,los datos que no estan disponibles toman el valor 0.

-Las columnas que estan anidadas que son genres,production_companies,belongs_to_collection,production_countries,spoken_languages las 
desanidamos para llegar a los valores.

### 2. Desarrollo API :

Archivo principal: **[main.py](main.py)**
- Se realizó el proceso de disponibilización de la información mediante el framework FastAPI.

### 3. Etapa del proceso EDA:
Archivo principal: **[EDA-Recoemdacion](EDA.ipynb)**
Se realizaron las tareas de MVP requeridas:
 
Se analizaron los valores faltantes.
    
 Se analizo los valores atipicos de las columnas popularity, runtime, vote_averange 
 Se llego a la conclusion que mayoria de peliculas no son muy populares 
 segun al distribucion del primer diagrama, tambien podemos ver que la duracion 
 de la mayoria de peliculas esta dentro de un rango alredor de los 100 minutos y 
 las calificaciones el tercer diagrama muestra que la mayoria de 
 las peliculas tienen una calificacion promedio entre 5 y 8. 
        
Se realizó un Mapa de calor de la matriz de correlacion 
 Llegamos a la conclusion
 - Aunque una pelicula sea muy popular no necesariamente tiene mejores o peores calificaciones que una pelicula menos popular 
 - Tambien podemos ver que la duracion de una pelicula no tiene una influencia relevante a su popularidad.
       
 Se realizó un Grafico de dispersion para evaluar la relacion entre popularidad, promedio de votos y año de lanzamiento 
 Llegamos a la conclusion:
- El publico tiende a disfrutar mas las peliculas más nuevas, pero la popularidad no necesariamente se relaciona con la puntacion de votos mas alta.
 - Tambien podemos ver algunos valores atipicos, ya que hay algunas peliculas antiguas que tienen una calificacion mas alta que algunas peliculas mas recientes.

### 4. Etapa del Sistema de Recomendación :
Archivo principal: **[EDA- Recomendacion](recomendacion.ipynb)**
Éste consiste en recomendar películas a los usuarios basándose en películas similares, por lo que se debe encontrar la similitud entre las película y el resto de películas, se ordenarán y devolverá un diccionario de Python con 5 valores, cada uno siendo el string. Fue deployado como una función adicional de la API anterior y se llama recomendacion(titulo: str).


**[Link del Deployment](https://pi-ml-ops4.onrender.com/docs)**
