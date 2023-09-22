from fastapi import FastAPI
import pandas as pd
from urllib.parse import unquote
from fastapi.responses import JSONResponse
from sklearn.metrics.pairwise import cosine_similarity

#Instancio la app
app = FastAPI()

#leo los archivos a consumir en las funciones
df_reviews = pd.read_parquet('Data/user_reviews.parquet')
df_generos = pd.read_parquet('Data/generos.parquet')
df_generos_horas = pd.read_parquet('Data/generos_horas.parquet')
df_userdata = pd.read_parquet('Data/df_userdata.parquet')
df_developer = pd.read_parquet('Data/df_developer.parquet')
df_modelo = pd.read_parquet('Data/df_modelo_final.parquet')
df_similitudes = pd.read_parquet('Data/matriz_similitud.parquet')

#FUNCIONES:

#userdata
'''Esta función devuelve información sobre un usuario según su 'user_id'. Args:
    user_id (str): Identificador único del usuario.
    
    Returns:
        dict: Un diccionario que contiene información sobre el usuario.
            - 'Total spent by user' (int): Cantidad de dinero gastado por el usuario.
            - 'Recommendation percentage' (float): Porcentaje de recomendaciones realizadas por el usuario.
            - 'Items quantity' (int): Cantidad de items que tiene el usuario.
            '''
            
@app.get("/userdata/{user_id}", name = "userdata (user_id)")
async def userdata(user_id:str):
    
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


#countreviews
'''Esta función devuelve estadísticas sobre las reviews realizadas por los usuarios entre dos fechas.
         
    Args:
        start_date (str): Fecha de inicio para filtrar la información (se debe ingresar el año).
        fecha_fin (str): Fecha de fin para filtrar la información (se debe ingresar el año).
    
    Returns:
        dict: Un diccionario que contiene estadísticas de las reviews entre las fechas especificadas.
            - 'Total users who made reviews' (int): Cantidad de usuarios que realizaron reviews entre las fechas.
            - 'Recommendation percentage' (float): Porcentaje de recomendaciones positivas (True) entre las reviews realizadas.
    '''
    
@app.get("/countreviews/{start_date},{end_date}", name = "countreviews (start_date, end_date)")
async def count_reviews(start_date: str, end_date: str):
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


#generos
'''Esta función devuelve la posición de un género de videojuego en un ranking basado en la cantidad de horas jugadas.
         
    Args:
        genero (str): Género del videojuego.
    
    Returns:
        dict: Un diccionario que contiene la posición del género en el ranking.
            - 'rank' (int): Posición del género en el ranking basado en las horas jugadas.
    '''
    
@app.get("/generos/{genero}", name = "generos (genero)")
async def genre_ranking(genero: str):
    
    # Calculo el ranking basado en la suma de "playtime_forever"
    df_generos['Rank'] = df_generos['playtime_forever'].rank(method='min', ascending=False)

    # Obtengo el puesto del género en el ranking
    rank = round(df_generos[df_generos['genres'] == genero]['Rank'].values[0])
    result = {'The rank of the genre is':rank}
    return result


#userforgenre
'''
    Esta función devuelve el top 5 de usuarios con más horas de juego en un género específico, junto con su URL de perfil y ID de usuario.
         
    Args:
        genero (str): Género del videojuego.
    
    Returns:
        Lista: Una lista que contiene el top 5 de usuarios con más horas de juego en el género dado, junto con su URL de perfil y ID de usuario.
            - 'user_id' (str): ID del usuario.
            - 'user_url' (str): URL del perfil del usuario.
    '''

@app.get("/userforgenre/{genero}", name = "userforgenre (genero)")
async def userforgenre(genero: str):
     
    # Filtrar el DataFrame por el género deseado
    genre_df = df_generos_horas[df_generos_horas['genres'].str.contains(genero, case=False, na=False)]

    # Ordenar en orden descendente por horas de juego y obtener el top 5
    top_5_users = genre_df.sort_values(by='playtime_forever', ascending=False).head(5)

    return top_5_users[['user_id', 'user_url']]



#developer
'''
    Esta función devuelve información sobre una empresa desarrolladora de videojuegos.
         
    Args:
        developer (str): Nombre del desarrollador de videojuegos.
    
    Returns:
        dict: Un diccionario que contiene información sobre la empresa desarrolladora.
            - 'year' (dict): año.
            - 'Items Qty' (dict): Cantidad de items desarrollados por año.
            - 'Free percentage' (dict): Porcentaje de contenido gratuito por año según la empresa desarrolladora.
    '''

@app.get("/developer/{developer}", name="developer (developer)")
async def developer(developer: str):
    # Filtrar el DataFrame por el desarrollador dado luego de decodificar el nombre
    decoded_name = unquote(developer)
    developer_data = df_developer[df_developer['developer'] == decoded_name]

    if developer_data.empty:
        return JSONResponse(content={"message": "Desarrollador no encontrado"}, status_code=404)

    # Crear un DataFrame con los resultados para el desarrollador
    resultados = {
        'Year': developer_data['release_year'].tolist(),
        'Items Qty': developer_data['item_id_x'].tolist(),
        'Free percentage': (developer_data['items_free_por_anio'] / developer_data['item_id_x'] * 100).fillna(0).tolist()
    }

    # Devolver los resultados como una respuesta JSON
    return JSONResponse(content=resultados)


#sentiment_analysis
'''Realiza un análisis de sentimiento en base al año ingresado.
    
    Args:
        year (str): El año para filtrar las reseñas.
    
    Returns:
        dict: Un diccionario con el recuento de categorías de sentimiento.
    '''

@app.get("/sentiment_analysis/{year}", name="sentiment_analysis (year)")
async def sentiment_analysis(year: int):
   
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


#modelo_recomendacion
'''
    Muestra una lista de juegos similares a un juego dado.

    Args:
        ID (INT): El ID del juego para el cual se desean encontrar juegos similares.

    Returns:
        df: Un diccionario con 5 nombres de juegos recomendados.

    '''

@app.get("/modelo_recomendacion/{id}", name="modelo_recomendacion (id)")
async def recomendacion_juego(id):
    
    id = int(id)
    # Filtrar el juego de entrada por su ID
    juego_seleccionado = df_modelo[df_modelo['id'] == id]
    
    if juego_seleccionado.empty:
        return "El juego con el ID especificado no existe en la base de datos."
    
    # Obtener las puntuaciones de similitud del juego de entrada con otros juegos
    similarity_scores = df_similitudes[df_modelo[df_modelo['id'] == id].index[0]]
    
    # Obtener los índices de los juegos más similares (excluyendo el juego de entrada)
    indices_juegos_similares = similarity_scores.argsort()[::-1][1:5+1]
    
    # Obtener los nombres de los juegos recomendados
    juegos_recomendados = df_modelo.iloc[indices_juegos_similares]['app_name'].tolist()
    
    return juegos_recomendados




