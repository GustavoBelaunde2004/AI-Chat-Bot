from services import Services
import uvicorn
from fastapi import FastAPI
from pywa_async import WhatsApp,types
from database import Database

# Start app
app = FastAPI()
services = Services()
database = Database()

# Set Whatsapp client
wa = WhatsApp(
    phone_id= services.settings.phone_id,
    token= services.settings.graph_api_token,
    server=app,
    verify_token= services.settings.webhook_verify_token,
)

# Response messages
@wa.on_message()
async def message_handler(_: WhatsApp, msg: types.Message): 
    services.logger.info('A MESSAGE have been arrived')
    response = await services.webhook(msg)
    return response

@wa.on_callback_button()
async def handle_button_click(_: WhatsApp, callback_query: types.CallbackButton):
    services.logger.info('A BUTTON ANSWER have been arrived')
     # Verificar el formato de callback_data
    data_parts = callback_query.data.split(":")

    option = data_parts[1]

    services.logger.info(f"Preference: {option}")

    await database.update_timestamp_and_preference(user_id=callback_query.from_user.wa_id, timestamp=callback_query.timestamp, preference=option)

    # Registrar el resultado
    services.logger.info(f"Saved preference: user_id={callback_query.from_user.wa_id}, option={option}")

    await callback_query.reply_text("He guardado tu preferencia de respuesta, por favor haga su pregunta")

#Run app
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
