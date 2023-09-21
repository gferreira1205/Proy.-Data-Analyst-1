# Prueba de concepto para proyecto de Steam
## Introducción
Este proyecto simula el rol de un MLOps Engineer, es decir, la combinación de un Data Engineer y Data Scientist, para la plataforma multinacional de videojuegos Steam. Para su desarrollo, se entregan unos datos y se solicita un Producto Mínimo Viable (MVP) que muestre una API deployada en un servicio en la nube y la aplicación de modelos de Machine Learning, en el que se solicita crear un modelo de recomendación para usarios.

## Contexto
Steam es una plataforma de distribución digital de videojuegos desarrollada por Valve Corporation. Fue lanzada en septiembre de 2003 como una forma para Valve de proveer actualizaciones automáticas a sus juegos, pero finalmente se amplió para incluir juegos de terceros. Según las cifras de SteamDB, la plataforma alcanzó en enero de 2023 las 33.078.963 personas conectadas a la vez. Esta cifra es la más alta de la historia de Steam, así que supone un nuevo récord en la cantidad de usuarios simultáneos usando el programa al mismo tiempo. SteamDB también han informado acerca de la cantidad de jugadores simultáneos que se registraron en ese momento: más de 10 millones de personas estaban jugando a la vez por primera vez en la historia de la plataforma, marcando otro récord para Valve.

## Datos
Para este proyecto se proporcionaron tres archivos JSON comprimidos a gz:

**steam_games.json:** es un dataset que contiene datos relacionados con los juegos en sí, como los títulos, el desarrollador, los precios, características técnicas, etiquetas, reviews, entre otros datos.

**user_reviews.json:** es un dataset que contiene los comentarios que los usuarios realizaron sobre los juegos que consumen, además de datos adicionales como si recomiendan o no ese juego, emoticones de gracioso y estadísticas de si el comentario fue útil o no para otros usuarios. También presenta el id del usuario que comenta con su url del perfil y el id del juego que comenta.

**users_items.json:** es un dataset que contiene información sobre los juegos que juegan todos los usuarios, así como el tiempo acumulado que cada usuario jugó a un determinado juego.

En el documento [Diccionario de datos](Diccionario de datos.md) se encuetran los detalles de cada una de las variables de los conjuntos de datos.


