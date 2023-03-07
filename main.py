import pandas as pd
import transformation as tr
import json
from fastapi import FastAPI

#Titulo y descripción de la API
app = FastAPI(title= 'Movies and Series database',
              description= 'Through this API you can find the movies/series of the platforms: Amazon, Disney Plus, Hulu and Netflix',
              )

# welcome
@app.get('/')
async def index():
    return {"Welcome!!!"}

@app.get('/about')
async def about():
    return 'Proyecto Data Engineer para SoyHenry'

# files load
platforms = {'amazon': tr.df_amazon, 'disney':tr.df_disney, 'hulu': tr.df_hulu, 'netflix':tr.df_netflix}

# general file load
@app.on_event('startup')
async def startup():
    global df
    df= pd.read_csv(r'df_final.csv')
    

#QUERY

# 1) Number of times a keyword appears in the title of movies/series, by platform
@app.get('/keyword_quantity')
async def keyword_quantity (data_frame:str, keyword:str):
    contador = 0
    lista = []
    for palabra in platforms[data_frame].title:
        palabra = palabra.split()
        for elemento in palabra:
            lista.append(elemento)
    contador = lista.count(keyword)
    return contador

# 2) Number of films by platform with a score greater than XX in a given year
@app.get('/film_by_score')
async def film_by_score(data_frame:str, anio:int, puntaje:int):
    return tr.film_by_score(platforms[data_frame], anio, puntaje)

# 3) Second highest scoring film for a given platform, based on alphabetical order of titles
@app.get('/second_max')
def second_max(data_frame:str):
    return json.loads(tr.second_max(platforms[data_frame]))

# 4) Film that lasted the longest according to year, platform and type of duration
@app.get('/max_duration')
def max_duration(data_frame:str, tipo:str):
    return json.loads(tr.max_duration(platforms[data_frame], tipo))

# 5) Number of series and movies by score
@app.get('/movies_series_byscore')
def movies_series_byscore (data_frame):
    return json.loads(tr.movies_series_byscore(platforms[data_frame]))