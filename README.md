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

Uno de los pedidos para este proyecto fue aplicar un análisis de sentimiento a los reviews de los usuarios. Para ello se creó una nueva columna llamada 'sentimentiento' que reemplaza a la columna que contiene los reviews donde clasifica los sentimientos de los comentarios con la siguiente escala:

0 si es malo,
1 si es neutral o esta sin review
2 si es positivo.  

Dado que el objetivo de este proyecto es realizar una prueba de concepto, se realiza un análisis de sentimiento básico utilizando NLTK (Natural Language Toolkit) que es una biblioteca de procesamiento de lenguaje natural (NLP) en Python. Esta librería proporciona una serie de herramientas y recursos para tareas de procesamiento de lenguaje natural (NLP) como tokenización, etiquetado de partes del discurso, análisis de sentimientos, análisis de texto, extracción de información y más. El objetivo de esta metodología es asignar un valor numérico a un texto, en este caso a los comentarios que los usuarios dejaron para un juego determinado, para representar si el sentimiento expresado en el texto es negativo, neutral o positivo.

Por otra parte, y bajo el mismo criterio de optimizar los tiempos de respuesta de las consultas en la API y teniendo en cuenta las limitaciones de almacenamiento en el servicio de nube para deployar la API, se realizaron dataframes auxiliares para cada una de las funciones solicitadas. En el mismo sentido, se guardaron estos dataframes en formato parquet que permite una compresión y codificación eficiente de los datos.

Todos los detalles del desarrollo se pueden ver en el Jupyter Notebook [Data Engineer](JupyterNotebooks/Data_Engineer.ipynb)


### Análisis exploratorio de los datos (EDA)

Se decidió realizar el EDA al conjunto de datos steam_games con el objetivo de identificar las variables que se pueden utilizar en la creación del modelo de recmendación así como de datos duplicados, nulos y outliers. Para ello se utilizó la librería Pandas para la manipulación de los datos y las librerías Matplotlib y Seaborn para la visualización.

En particular para el modelo de recomendación, se terminó eligiendo construir un dataframe específico con las siguientes columnas:  'app_name','id','genres'.

El desarrollo de este análisis se encuentra en el Jupyter Notebook EDA [EDA](JupyterNotebooks/EDA.ipynb)


### Modelo de aprendizaje automático

Se creó un modelo de recomendación, que genera una lista de 5 juegos ingresando el id de un producto. Este modelo tiene una relación ítem-ítem, esto es, se toma un juego y en base a que tan similar es ese juego con el resto de los juegos se recomiendan similares.

Para medir la similitud entre los juegos (item_similarity) se utilizó la similitud del coseno que es una medida comúnmente utilizada para evaluar la similitud entre dos vectores en un espacio multidimensional. En el contexto de sistemas de recomendación y análisis de datos, la similitud del coseno se utiliza para determinar cuán similares son dos conjuntos de datos o elementos, y se calcula utilizando el coseno del ángulo entre los vectores que representan esos datos o elementos.

El desarrollo para la creación de los dos modelos se presenta en el Jupyter Notebook [Modelo Recomendación](JupyterNotebooks/Modelo_Recomendacion.ipynb).


### Desarrollo de API

Para el desarrolo de la API se decidió utilizar el framework FastAPI, creando las siguientes funciones:  

***userdata:*** Esta función tiene por parámentro 'user_id' y devulve la cantidad de dinero gastado por el usuario, el porcentaje de recomendaciones que realizó sobre la cantidad de reviews que se analizan y la cantidad de items que consume el mismo.  

**count_reviews:** En esta función se ingresan dos fechas entre las que se quiere hacer una consulta y devuelve la cantidad de usuarios que realizaron reviews entre dichas fechas y el porcentaje de las recomendaciones positivas (True) que los mismos hicieron.  

**generos:** Esta función recibe como parámetro un género de videojuego y devuelve el puesto en el que se encuentra dicho género sobre un ranking de los mismos analizando la cantidad de horas jugadas para cada uno.  

**userforgenre:** Esta función recibe como parámetro el género de un videojuego y devuelve el top 5 de los usuarios con más horas de juego en el género ingresado, indicando el id del usuario y el url de su perfil.  

**developer:** Esta función recibe como parámetro 'developer', que es la empresa desarrolladora del juego, y devuelve la cantidad de items que desarrolla dicha empresa y el porcentaje de contenido Free por año por sobre el total que desarrolla.  

**sentiment_analysis:** Esta función recibe como parámetro el año de lanzamiento de un juego y según ese año devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento, como Negativo, Neutral y Positivo.  

**modelo_recomendacion** Esta función recibe como parámetro el nombre de un juego y devuelve una lista con 5 juegos recomendados similares al ingresado.  

El código para generar la API así como sus finciones, se encuentra en el archivo [Main](main.py). En caso de querer ejecutar la API desde localHost se deben seguir los siguientes pasos:

Clonar el proyecto haciendo git clone https://github.com/gferreira1205/Proy.-Data-Analyst-1.git.
Preparación del entorno de trabajo en Visual Studio Code:
Crear entorno Python -m venv env en caso de requerirse.
Ingresar al entorno haciendo venv\Scripts\activate
Instalar dependencias con pip install -r requirements.txt
Ejecutar el archivo main.py desde consola activando uvicorn. Para ello, hacer uvicorn main:app --reload
Hacer Ctrl + clic sobre la dirección http://XXX.X.X.X:XXXX (se muestra en la consola).
Una vez en el navegador, agregar /docs para acceder a ReDoc.
En cada una de las funciones hacer clic en Try it out y luego introducir el dato que requiera o utilizar los ejemplos por defecto. Finalmente Ejecutar y observar la respuesta.

# Deployment

Para el deploy de la API se seleccionó la plataforma Render que es una nube unificada para crear y ejecutar aplicaciones y sitios web, permitiendo el despliegue automático desde GitHub.

Se generó un nuevo WebService en render.com, conectado al presente repositorio.  

Finalmente, el servicio queda corriendo en https://pi1-games.onrender.com/.  

Video

En este video se explica brevemente este proyecto mostrando el funcionamiento de la API.






