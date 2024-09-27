import datetime
import os
import re
import aiohttp
from config import Settings, get_settings
from logger import get_logger
from typing import Optional
from bot_aliado import BotAliado
from speech import Speech
import tempfile
import soundfile as sf
from scipy.signal import resample
import numpy as np
from pywa_async import types 
from database import Database

class Services:
    def __init__(self):
        self.settings: Settings = get_settings()
        self.logger = get_logger(__name__)
        self.bot_aliado: BotAliado = BotAliado()
        self.speech: Speech = Speech()
        self.database: Database = Database()

    async def webhook(self, msg: types.Message):
        async with aiohttp.ClientSession() as session:
            msg_user_id = msg.from_user.wa_id # Obtener el ID del usuario
            msg_timestamp = msg.timestamp  # Obtener la marca de tiempo del mensaje

            #debug
            await msg.react("👍")
            self.logger.info(f"USER_ID: {msg_user_id}")
            self.logger.info(f"TIME: {msg_timestamp}" )

            #Obtener info guardada del usuario
            user_info = await self.database.get_user_info(msg_user_id) #DA EL TIMEOUT ERROR ACA

            #debug
            self.logger.info(f'user info: {user_info}')
            #await msg.reply_text(f'user info: {user_info}')
            
            #obterner preferencia
            preference = await self.get_preference(user_info,msg_user_id,msg_timestamp,msg)
            
            if preference is None:
                return None

            #debug
            self.logger.info(f"preferencia 1 : {preference}")

            if msg.type == "audio":
                if msg.audio.voice:
                    await msg.reply_text("Dame un momento")
                    message = await self.get_text_from_audio(msg)
                    self.logger.info(f'Message: {message}')
                    if 'Hola' in message or 'hola' in message:
                        conversation_id = await self.bot_aliado.start_conversation(session)
                        await msg.react("👋")
                        if preference == "text":
                            greeting_response = (f"""¡Hola {msg.from_user.name}! 😊 Soy el asistente virtual IBK ¿En qué puedo ayudarte hoy? Puedo guiarte sobre *consultas relacionadas a campañas y Plin*. Cuenta conmigo 🙌""")
                        else:
                            greeting_response = (f"""¡Hola {msg.from_user.name}! 😊 Soy el asistente virtual IBK ¿En qué puedo ayudarte hoy? Puedo guiarte sobre *consultas relacionadas a campañas y Plin*. Cuenta conmigo 🙌""")
                            greeting_response = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251*]', '', greeting_response)
                            await self.reply_audio(msg=msg, response= greeting_response)
                            self.logger.info('Audio response sent successfully')
                    elif 'Cambiar respuesta' in message or "cambiar respuesta" in message:
                        await self.send_preference_buttons(msg)
                    else:
                        #ANADIR LOGICA PARA SPLIT SI RESPUESTA ES MUY LARGA
                        conversation_id = await self.bot_aliado.get_conversation_history(session=session)
                        if conversation_id == None:
                            conversation_id = await self.bot_aliado.start_conversation(session=session)
                        response = await self.bot_aliado.send_question(conversation_id= conversation_id,
                                                                        question= message,session=session)
                        if preference == "audio":
                            await self.reply_audio(msg=msg, response= response)
                            self.logger.info('Audio response sent successfully')
                        else:
                            await msg.reply(response, preview_url=True)
                            self.logger.info('Text response sent successfully')   

            elif msg.type == "text":
                message = msg.text
                if 'Hola' in message or 'hola' in message:
                        conversation_id = await self.bot_aliado.start_conversation(session)
                        await msg.react("👋")
                        if preference == "text":
                            greeting_response = (f"""¡Hola {msg.from_user.name}! 😊 Soy el asistente virtual IBK ¿En qué puedo ayudarte hoy? Puedo guiarte sobre *consultas relacionadas a campañas y Plin*. Cuenta conmigo 🙌""")
                            await msg.reply(greeting_response, preview_url=True)
                            self.logger.info('Text response sent successfully')   
                        else:
                            greeting_response = (f"""¡Hola {msg.from_user.name}! 😊 Soy el asistente virtual IBK ¿En qué puedo ayudarte hoy? Puedo guiarte sobre *consultas relacionadas a campañas y Plin*. Cuenta conmigo 🙌""")
                            greeting_response = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251*]', '', greeting_response)
                            await self.reply_audio(msg=msg, response= greeting_response)
                            self.logger.info('Audio response sent successfully')
                elif 'Cambiar respuesta' in message or "cambiar respuesta" in message:
                    await self.send_preference_buttons(msg)
                else:
                    conversation_id = await self.bot_aliado.get_conversation_history(session=session)
                    if conversation_id == None:
                        conversation_id = await self.bot_aliado.start_conversation(session=session)
                    response = await self.bot_aliado.send_question(conversation_id= conversation_id,
                                                                    question= message,session=session)
                    if preference == "audio":
                        await self.reply_audio(msg=msg, response= response)
                        self.logger.info('Audio response sent successfully')
                    else:
                        await msg.reply(response, preview_url=True)
                        self.logger.info('Text response sent successfully')   
    
    async def reply_audio(self, msg: types.Message, response: str) -> bool:
        """Converts the text response to audio and replies it 

        Args:
            msg (types.Message): The message it is going to reply to
            response (str): The text is going to reply with as audio

        Returns:
            bool: Returns True if the audio is sent successfully
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_path = os.path.join(temp_dir, 'audio_temp.mp4')
            audio_path2 = os.path.join(temp_dir, 'audio_temp.mp3')
            audio_check = self.speech.text_to_speech(text=response, output_file=audio_path)
            if audio_check:
                try:
                    convert_status = self.convert_audio(audio_path, audio_path2)
                    if convert_status:
                        await msg.reply_audio(audio=audio_path2, mime_type='audio/mpeg')
                        self.logger.info('Audio response sent successfully')
                        return True
                except Exception as e:
                    self.logger.error(f'Error sending audio response: {e}')
                    return False
            else:
                self.logger.error('There was a problem generating audio response.')
                return False
            
    def convert_audio(self, input_path: str, output_path: str) -> bool:
        """Converts an audio file from mp4 format to mp3.

    Args:
        input_path (str): The file path of the input audio file.
        output_path (str): The file path where the converted audio file will be saved.

    Returns:
        bool: True if the audio conversion is successful.
        """
        try:
            data, samplerate = sf.read(input_path)
            sf.write(output_path, data, samplerate)
            self.logger.info('Audio converted successfully')
            return True
        except Exception as e:
            self.logger.error(f'Error while converting audio file. Error description: {str(e)}')
            return False
        
    async def get_text_from_audio(self, msg: types.Message) -> Optional[str]: 
        """Downloads the audio from the Message and transcribes it

        Args:
            msg (types.Message): The audio message that will be transcribed

        Returns:
            Optional[str]: The text transcribed from the audio
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                audio_path = os.path.join(temp_dir, 'audio_temp.wav')
                audio_file = await msg.audio.download(path=temp_dir,filename='audio_temp.opus')

                status_opus = os.stat(audio_file)
                self.logger.info(f'Audio status opus: {status_opus}')

                self.logger.info(f'Audio downloaded successfully in {audio_file}')
                audio_check = self.convert_audio_to_wav(audio_file, audio_path)

                status_wav = os.stat(audio_path)
                self.logger.info(f'Audio status wav: {status_wav}')

                if audio_check:
                    self.logger.info('Audio converted')
                    audio_text = self.speech.audio_to_text(audio_file_path=audio_path)
                    self.logger.info('Transcription finished successfully')
                    self.logger.info(f'Transcription: {audio_text}')
                    return audio_text
            except Exception as e:
                self.logger.error(f'Error while transcribing audio. Error description: {str(e)}')
                return None
            
    def convert_audio_to_wav(self, input_path: str, output_path: str) -> bool:
        """Convertes an Opus audio to a Wav audio

        Args:
            input_path (str): Path of the Opus audio
            output_path (str): Path of the converted Wav audio

        Returns:
            bool: True if conversion is succesful
        """
        try:
            # Leer el archivo de audio original
            data, samplerate = sf.read(input_path)
            
            # Verificar si el archivo ya está en el formato deseado
            if data.dtype != 'int16':
                # Convertir a PCM de 16 bits
                data = np.int16(data * 32767)
            
            # Asegurar que la frecuencia de muestreo sea de 16000 Hz
            if samplerate != 16000:
                # Resamplear el audio (puedes usar librosa o scipy para esto, aquí un ejemplo simple con scipy)
                
                number_of_samples = round(len(data) * float(16000) / samplerate)
                data = resample(data, number_of_samples)
                samplerate = 16000
            
            # Escribir el archivo de audio en formato WAV con PCM de 16 bits
            sf.write(output_path, data, samplerate, subtype='PCM_16')
            return True
        except Exception as e:
            print(f'Error while converting audio file. Error description: {str(e)}')
            return False
    
    async def get_preference(self,user_info,msg_user_id,msg_timestamp,msg):
        if isinstance(msg_timestamp, datetime.datetime):
            time = msg_timestamp.timestamp()

        preference = None

        if user_info:
            stored_timestamp, stored_preference = user_info
            if isinstance(stored_timestamp, datetime.datetime):
                stored_time = stored_timestamp.timestamp()

            time_diff = (datetime.datetime.fromtimestamp(time) - datetime.datetime.fromtimestamp(stored_time)).total_seconds()

            if time_diff > 3600:  # 1800 seconds = 30 minutes

                # Send button to choose preference and save it
                await self.send_preference_buttons(msg)
            else:
                preference = stored_preference
                # Update timestamp
                await self.database.update_timestamp_and_preference(msg_user_id, msg_timestamp, preference)
        else:
            await self.database.save_id_time_preference_to_db(msg_user_id,msg_timestamp,preference)
            # Send button to choose preference
            await self.send_preference_buttons(msg)
        return preference

    #BOTON
    async def send_preference_buttons(self, msg: types.Message):
        return await msg.reply_text(
             text=f"¡Hola {msg.from_user.name}! 😊 Soy el asistente virtual IBK. Puedo guiarte sobre *consultas relacionadas a campañas y Plin*. Por favor elige como quisieras que te responda, y en caso desee cambiarlo denuevo escriba \"Cambiar respuesta\"",
        buttons=[
            types.Button(title="Texto", callback_data="option:text"),
            types.Button(title="Audio", callback_data="option:audio")
        ]
    )

    def split_text(self,text:str, max_length):
        """
        Divide el texto en partes de longitud máxima max_length.
        Args:
            text (str): Texto a dividir.
            max_length (int): Longitud máxima de cada parte.
        Returns:
            List[str]: Lista de partes del texto.
        """
        # Divide el texto en palabras
        words = text.split()
        parts = []
        current_part = []

        for word in words:
            # Si agregar la palabra excede la longitud máxima, guarda la parte actual y comienza una nueva
            if len(" ".join(current_part + [word])) > max_length:
                parts.append(" ".join(current_part))
                current_part = [word]
            else:
                current_part.append(word)

        # Agrega la última parte
        if current_part:
            parts.append(" ".join(current_part))

        return parts
    
    