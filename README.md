# AI-Chat-Bot
Este proyecto es un bot de WhatsApp diseñado para interactuar con los usuarios mediante mensajes de texto y de voz. El bot está desplegado en un Azure Web App Service y utiliza Bot ALiado API creada con OpenAI para responder preguntas acerca de Campañas y Plin de Interbank. El bot también almacena información de los usuarios en una base de datos SQL en Azure.
## Pasos previos
### APIS
1. Bot Aliado API:
    1. Registrarse en [Bot Aliado API](https://aci-aliado-api.politebeach-527e58d4.eastus2.azurecontainerapps.io/) y obtener un API key.
2. Whatsapp Cloud API:
    1. Registrarse en [Meta for Developers](https://developers.facebook.com/?no_redirect=1)
    2. Crear una aplicacion y seguir pasos para obtener un API key.
3. Azure Speech API
    1. Registrarse en [Azure Speech](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/) y obtener API key.
### Requerimientos python
1. Instalar el archivo requirements.txt
2. Crear el archivo ***.env*** según el template.
### Requerimientos en Azure Web App Service
1. Definir Startup Commnad: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app

## Sobre el código
-***app.py***: Este archivo configura la aplicación FastAPI y los manejadores de eventos de WhatsApp.

-***bot_aliado.py***: Contiene la lógica para interactuar con la API de Bot Aliado.

-***database.py***: Maneja las operaciones con la base de datos SQL de Azure utilizando aioodbc.

-***services.py***: Contiene funciones auxiliares, incluyendo la lógica para manejar las interacciones del bot, convertir texto a audio, y más.

-***config.py***: Administra la configuración de la aplicación, cargando los valores desde el archivo .env.

-***logger.py***: Configura y proporciona un logger para la aplicación.

-***speech.py***: Utiliza servicios externos para convertir texto a audio y maneja la manipulación de archivos de audio.
