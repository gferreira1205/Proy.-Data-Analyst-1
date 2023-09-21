# Prueba de concepto para proyecto de Steam Games
## Introducción
Este proyecto simula el rol de un MLOps Engineer, es decir, la combinación de un Data Engineer y Data Scientist, para la plataforma multinacional de videojuegos Steam. Para su desarrollo, se entregan unos datos y se solicita un Producto Mínimo Viable (MVP) que muestre una API deployada en un servicio en la nube y la aplicación de modelos de Machine Learning, en el que se solicita crear un modelo de recomendación para usarios.

## Contexto
Steam es una plataforma de distribución digital de videojuegos desarrollada por Valve Corporation. Fue lanzada en septiembre de 2003 como una forma para Valve de proveer actualizaciones automáticas a sus juegos, pero finalmente se amplió para incluir juegos de terceros. Según las cifras de SteamDB, la plataforma alcanzó en enero de 2023 las 33.078.963 personas conectadas a la vez. Esta cifra es la más alta de la historia de Steam, así que supone un nuevo récord en la cantidad de usuarios simultáneos usando el programa al mismo tiempo. SteamDB también han informado acerca de la cantidad de jugadores simultáneos que se registraron en ese momento: más de 10 millones de personas estaban jugando a la vez por primera vez en la historia de la plataforma, marcando otro récord para Valve.

## Datos
Para este proyecto se proporcionaron tres archivos JSON comprimidos a gz:

**steam_games.json:** es un dataset que contiene datos relacionados con los juegos en sí, como los títulos, el desarrollador, los precios, características técnicas, etiquetas, reviews, entre otros datos.  

**user_reviews.json:** es un dataset que contiene los comentarios que los usuarios realizaron sobre los juegos que consumen, además de datos adicionales como si recomiendan o no ese juego, emoticones de gracioso y estadísticas de si el comentario fue útil o no para otros usuarios. También presenta el id del usuario que comenta con su url del perfil y el id del juego que comenta.  

**users_items.json:** es un dataset que contiene información sobre los juegos que juegan todos los usuarios, así como el tiempo acumulado que cada usuario jugó a un determinado juego.  

En el documento [Diccionario de datos](JupyterNotebooks/Diccionario_de_datos.md) se encuetran los detalles de cada una de las variables de los conjuntos de datos.

## Tareas desarrolladas
### Transformaciones

Se realizó la extracción, transformación y carga (ETL) de los tres conjuntos de datos entregados. Dos de los conjuntos de datos se encontraban anidados, es decir había columnas con diccionarios o listas de diccionarios, por lo que aplicaron distintas estrategias para transformar las claves de esos diccionarios en columnas. Luego se rellenaron algunos nulos de variables necesarias para el proyecto, se borraron columnas con muchos nulos o que no aportaban al proyecto, para optimizar el rendimiento de la API y teneniendo en cuenta las limitaciones de almacenamiento del deploy. Para las transformaciones se utilizó la librería Pandas.

Los detalles del ETL se pueden ver en el archivo [Data Engineer](JupyterNotebooks/Data_Engineer.ipynb)

### Feature engineering

Uno de los pedidos para este proyecto fue aplicar un análisis de sentimiento a los reviews de los usuarios. Para ello se creó una nueva columna llamada 'sentiment_analysis' que reemplaza a la columna que contiene los reviews donde clasifica los sentimientos de los comentarios con la siguiente escala:

0 si es malo,
1 si es neutral o esta sin review
2 si es positivo.
Dado que el objetivo de este proyecto es realizar una prueba de concepto, se realiza un análisis de sentimiento básico utilizando TextBlob que es una biblioteca de procesamiento de lenguaje natural (NLP) en Python. El objetivo de esta metodología es asignar un valor numérico a un texto, en este caso a los comentarios que los usuarios dejaron para un juego determinado, para representar si el sentimiento expresado en el texto es negativo, neutral o positivo.

Esta metodología toma una revisión de texto como entrada, utiliza TextBlob para calcular la polaridad de sentimiento y luego clasifica la revisión como negativa, neutral o positiva en función de la polaridad calculada. En este caso, se consideraron las polaridades por defecto del modelo, el cuál utiliza umbrales -0.2 y 0.2, siendo polaridades negativas por debajo de -0.2, positivas por encima de 0.2 y neutrales entre medio de ambos.

Por otra parte, y bajo el mismo criterio de optimizar los tiempos de respuesta de las consultas en la API y teniendo en cuenta las limitaciones de almacenamiento en el servicio de nube para deployar la API, se realizaron dataframes auxiliares para cada una de las funciones solicitadas. En el mismo sentido, se guardaron estos dataframes en formato parquet que permite una compresión y codificación eficiente de los datos.

Todos los detalles del desarrollo se pueden ver en la Jupyter Notebook 01d_Feature_eng.

