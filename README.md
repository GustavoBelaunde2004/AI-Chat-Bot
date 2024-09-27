# AI-Chat-Bot
Este proyecto es un bot de WhatsApp diseñado para interactuar con los usuarios mediante mensajes de texto y de voz. El bot está desplegado en un Azure Web App Service y utiliza Bot ALiado API creada con OpenAI para responder preguntas acerca de Campañas y Plin de Interbank. El bot también almacena información de los usuarios en una base de datos SQL en Azure.

Pasos previos
APIS
Bot Aliado API:
Registrarse en Bot Aliado API y obtener un API key.
Whatsapp Cloud API:
Registrarse en Meta for Developers
Crear una aplicacion y seguir pasos para obtener un API key.
Azure Speech API
Registrarse en Azure Speech y obtener API key.
Requerimientos python
Instalar el archivo requirements.txt
Crear el archivo .env según el template.
Requerimientos en Azure Web App Service
Definir Startup Commnad: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
Sobre el código
-app.py: Este archivo configura la aplicación FastAPI y los manejadores de eventos de WhatsApp.

-bot_aliado.py: Contiene la lógica para interactuar con la API de Bot Aliado.

-database.py: Maneja las operaciones con la base de datos SQL de Azure utilizando aioodbc.

-services.py: Contiene funciones auxiliares, incluyendo la lógica para manejar las interacciones del bot, convertir texto a audio, y más.

-config.py: Administra la configuración de la aplicación, cargando los valores desde el archivo .env.

-logger.py: Configura y proporciona un logger para la aplicación.

-speech.py: Utiliza servicios externos para convertir texto a audio y maneja la manipulación de archivos de audio.
