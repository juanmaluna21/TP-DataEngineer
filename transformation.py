import pandas as pd
import json as json

def transformation (df,letras):
    df.rename(columns={'show_id':'id'},inplace= True) # renombro la columna "show_id" a "id"
    df['id'] = [letras + elemento for elemento in df['id']] # agrego la letra correspodiente
    df.set_index('id',inplace=True) # asigno a la columna "id" como indice
    df['rating'].fillna('G',inplace=True) # relleno los valores NaN de la columna "rating" con "G"
    df['date_added']= pd.to_datetime(df['date_added']) #cambio el formato de las fechas
    string_columns = [column for column in df.columns if df[column].dtype == 'object'] #elijo cual de las columnas es de tipo 'object'
    df[string_columns] = df.loc[:,string_columns].apply(lambda x: x.str.lower()) # transformo en minusculas a las columnas de tipo object
    df['duration'].fillna ('NaN NaN', inplace=True) #reemplazo el los valores faltantes de la columna duration por "NaN NaN" con el fin de poder dividirla depues
    duracion = df['duration'].str.split() #separo la columna "duration" en 2
    duration_int = [i[0] for i in duracion] # asigno los primeros valores a "duration_int"
    duration_type= [i[1] for i in duracion] # asigno los primeros valores a "duration_type"
    df.insert(9,'duration_int',duration_int) # inserto la columna "duration_int"
    df.insert(10,'duration_type',duration_type) # inserto la columna "duration_type"
    df.drop(columns= 'duration', inplace= True) # elimino la columna duration
    df['duration_type'].replace('seasons','season', inplace=True) # corrijo los valores "seasons" por "season" para tener un solo valor y facilite la busqueda
    return df

# Importación de archivos
df_disney = pd.read_csv (r'Datasets/disney_plus_titles-score.csv', encoding= 'UTF-8')
df_amazon = pd.read_csv (r'Datasets/amazon_prime_titles-score.csv', encoding= 'UTF-8')
df_hulu = pd.read_csv (r'Datasets/hulu_titles-score (2).csv', encoding= 'UTF-8')
df_netflix = pd.read_csv (r'Datasets/netflix_titles-score.csv', encoding= 'UTF-8')

# Aplicación de cambios
df_amazon = transformation (df_amazon,'a')
df_disney = transformation (df_disney,'d')
df_hulu = transformation (df_hulu,'h')
df_netflix = transformation (df_netflix,'n')


#PREGUNTAS
# 1) Number of times a keyword appears in the title of movies/series, by platform
def keyword_quantity (platform, keyword):
    count = 0
    list1 = []
    for word in platform.title:
        word = str(word).split()
        for element in word:
            list1.append(element)
    count = list1.count(keyword)
    return count
# 2) Number of films by platform with a score greater than XX in a given year
def film_by_score(platform, year, score):
    return len(platform[(platform['date_added'].dt.year== year) & (platform['score'] >= score)].value_counts())
# 3) Second highest scoring film for a given platform, based on alphabetical order of titles
def second_max(platform):
    return platform[platform['score']==platform['score'].max()].sort_values(by=['title']).iloc[1].to_json()
# 4) Film that lasted the longest according to year, platform and type of duration
def max_duration(platform, type):
    return platform[platform['duration_type']== type].sort_values(by= ['duration_int']).iloc[-1].to_json()
# 5) Number of series and movies by score
def movies_series_byscore (platform):
    return platform['rating'].value_counts().to_json()