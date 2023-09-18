from fastapi import FastAPI
import pandas as pd
from urllib.parse import unquote
from fastapi.responses import JSONResponse

app = FastAPI()

df_reviews = pd.read_parquet('Data/user_reviews.parquet')
df_generos = pd.read_parquet('Data/generos.parquet')
df_generos_horas = pd.read_parquet('Data/generos_horas.parquet')
df_userdata = pd.read_parquet('Data/df_userdata.parquet')
df_developer = pd.read_parquet('Data/df_developer.parquet')


@app.get("/userdata/{user_id}", name = "userdata (user_id)")
def userdata(user_id:str):
    # Filtro el DataFrame para obtener solo las filas del usuario específico
    user_data = df_userdata[df_userdata['user_id'] == user_id]

    # Calculo la cantidad de dinero gastado sumando el precio de todos los elementos comprados
    if user_data.empty:
        total_gasto = 0
    else: total_gasto = round(user_data['price'].sum(),2)
    
    user_reviews = df_reviews[df_reviews['user_id'] == user_id]
    
    if user_reviews.empty:
        recommendation_percentage = 0
    else:
        recommendation_percentage = round((user_reviews['recommend'].sum() / len(user_reviews)) * 100)
    
    # Obtiene la cantidad de elementos del usuario
    items_count = len(user_data)

    # Devuelve los resultados como un diccionario
    user_info = {
        'Total spent by user': total_gasto,
        'Recommendation percentage': f"{recommendation_percentage:}%",
        'Items quantity': items_count
    }
    
    return user_info


@app.get("/countreviews/{start_date},{end_date}", name = "countreviews (start_date, end_date)")
def count_reviews(start_date: str, end_date: str):
    # Convierte las fechas de inicio y fin a objetos datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filtra el DataFrame para obtener las reseñas en el rango de fechas
    filtered_df = df_reviews[(df_reviews['fecha_review'] >= start_date) & (df_reviews['fecha_review'] <= end_date)]

    # Cuenta la cantidad de usuarios que realizaron reseñas en el rango
    num_users = filtered_df['user_id'].nunique()
    
     # Filtra las reseñas que tienen 'reviews.recommend' igual a True
    positive_reviews = filtered_df[filtered_df['recommend']]

    # Calcula el porcentaje de recomendación en base a la columna 'reviews.recommend'
    recommend_percentage = round((positive_reviews.shape[0] / filtered_df.shape[0]) * 100)
    #recommend_percentage = (filtered_df['recommend'].sum() / filtered_df.shape[0]) * 100
    
    info = {
        'Total users who made reviews': f"{num_users} users",
        'Recommendation percentage': f"{recommend_percentage:}%",
    }
    return info


@app.get("/generos/{genero}", name = "generos (genero)")
def genre_ranking(genero: str):
    
    # Calculo el ranking basado en la suma de "playtime_forever"
    df_generos['Rank'] = df_generos['playtime_forever'].rank(method='min', ascending=False)

    # Obtengo el puesto del género en el ranking
    rank = round(df_generos[df_generos['genres'] == genero]['Rank'].values[0])
    result = {'The rank of the genre is':rank}
    return result


@app.get("/userforgenre/{genero}", name = "userforgenre (genero)")
def userforgenre(genero: str):
     
    # Filtrar el DataFrame por el género deseado
    genre_df = df_generos_horas[df_generos_horas['genres'].str.contains(genero, case=False, na=False)]

    # Ordenar en orden descendente por horas de juego y obtener el top 5
    top_5_users = genre_df.sort_values(by='playtime_forever', ascending=False).head(5)

    return top_5_users[['user_id', 'user_url']]



@app.get("/developer/{developer}", name="developer (developer)")
def developer(developer: str):
    
    # Filtramos el DataFrame por el desarrollador dado luego de decodificar el nombre
    decoded_name = unquote(developer)
    developer_df = df_developer[df_developer['developer'] == decoded_name]
    
    # Calculamos la cantidad de ítems gratuitos (Free) por año para el desarrollador
    items_free_por_anio = developer_df[developer_df['price'] == 0].groupby('release_year')['item_id_x'].nunique()
    
    # Calculamos la cantidad total de ítems por año para el desarrollador
    items_totales_por_anio = developer_df.groupby('release_year')['item_id_x'].nunique()
    
    # Rellenamos los años faltantes en el DataFrame de items_free_por_anio con ceros para que no arroje error el dataframe
    for year in items_totales_por_anio.index:
        if year not in items_free_por_anio.index:
            items_free_por_anio[year] = 0
    
    # Ordenamos el DataFrame por año
    items_free_por_anio = items_free_por_anio.sort_index()
    
    # Calculamos el porcentaje de contenido Free por año
    porcentaje_free = (items_free_por_anio / items_totales_por_anio) * 100
    
    # Creamos un DataFrame con los resultados
    resultados = {
        'Year': items_free_por_anio.index.tolist(),
        'Items Qty': items_totales_por_anio.values.tolist(),
        'Free percentage': porcentaje_free.values.tolist()
    }
    
    # Devolvemos los resultados como una respuesta JSON
    return JSONResponse(content=resultados)


@app.get("/sentiment_analysis/{year}", name="sentiment_analysis (year)")
def sentiment_analysis(year: int):
   
    # Filtra el DataFrame para obtener solo las reseñas del año dado
    reseñas_del_año = df_reviews[df_reviews['Año'] == year]
    
    # Cuenta la cantidad de registros para cada categoría de sentimiento
    sentimiento_counts = reseñas_del_año['sentimiento'].astype(int).value_counts()

    # Convierte los resultados a un diccionario con las etiquetas "Negative", "Neutral" y "Positive"
    resultado = {
        "Negative": int(sentimiento_counts.get(0, 0)),  # Valor 0 representa "Negative"
        "Neutral": int(sentimiento_counts.get(1, 0)),   # Valor 1 representa "Neutral"
        "Positive": int(sentimiento_counts.get(2, 0))   # Valor 2 representa "Positive"
    }

    return resultado




