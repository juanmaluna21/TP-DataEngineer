from fastapi import FastAPI
import pandas as pd

#Titulo y descripción de la API
app = FastAPI(title= 'Base de datos de Peliculas',
              description= 'A través de esta API se puede encontrar las peliculas/series de las plataformas: Amazon, Disney Plus, Hulu y Netflix',
              )

df= pd.read_csv(r'df_final.to_csv')

@app.get('/')
async def index ():
    return {"Bienvenido!!!"}

@app.get('about')
async def about():
    return 'Proyecto Data Engineer para SoyHenry'

@app.get('cantidad_keyword')
async def cantidad_keyword (data_frame: str, keyword: str):
    contador = 0
    lista = []
    for palabra in data_frame.title:
        palabra = palabra.split()
        for elemento in palabra:
            lista.append(elemento)
    contador = lista.count(keyword)
    return contador
