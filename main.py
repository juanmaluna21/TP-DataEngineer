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
async def keyword_quantity (platform:str, keyword:str):
    count = 0
    list1 = []
    for word in platforms[platform].title:
        word = word.split()
        for element in word:
            list1.append(element)
    count = list1.count(keyword)
    return count

# 2) Number of films by platform with a score greater than XX in a given year
@app.get('/film_by_score')
async def film_by_score(platform:str, year:int, score:int):
    return tr.film_by_score(platforms[platform], year, score)

# 3) Second highest scoring film for a given platform, based on alphabetical order of titles
@app.get('/second_max')
def second_max(platform:str):
    return json.loads(tr.second_max(platforms[platform]))

# 4) Film that lasted the longest according to year, platform and type of duration
@app.get('/max_duration')
def max_duration(platform:str, type:str):
    return json.loads(tr.max_duration(platforms[platform], type))

# 5) Number of series and movies by score
@app.get('/movies_series_byscore')
def movies_series_byscore (platform):
    return json.loads(tr.movies_series_byscore(platforms[platform]))