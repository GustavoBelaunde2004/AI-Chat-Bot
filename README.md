# AI-Chat-Bot
This project is a WhatsApp bot designed to interact with users through text and voice messages. The bot is deployed on an Azure Web App Service and uses Bot ALiado API created with OpenAI to answer questions about Interbank. The bot also stores user information in a SQL database on Azure.
## Previous steps
### APIS
1. Bot Aliado API:
    1. Request for a Bot Aliado API key.
2. Whatsapp Cloud API:
    1. Register in [Meta for Developers](https://developers.facebook.com/?no_redirect=1)
    2. Create an app and follow steps to obatin API key.
3. Azure Speech API
    1. Register in [Azure Speech](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/) and obtain API key.
### Python requirements
1. Install requirements.txt
2. Create ***.env*** file following the template.
### Azure Web App Service Requirements
1. Define Startup Commnad: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app

## Project Files Description

- **`app.py`**: Sets up the FastAPI application and the event handlers for WhatsApp.

- **`bot_aliado.py`**: Contains the logic to interact with the Bot Aliado API.

- **`config.py`**: Manages the application's configuration, loading values from the `.env` file.

- **`database.py`**: Manages operations with the Azure SQL database using `aioodbc`.

- **`logger.py`**: Sets up and provides a logger for the application.

- **`services.py`**: Contains helper functions, including logic to handle bot interactions, text-to-speech conversion, and more.

- **`speech.py`**: Uses external services to convert text to audio and handles audio file manipulation.

## Feel free to contact me if you have any questions!