import azure.cognitiveservices.speech as speechsdk
from config import Settings, get_settings
from logger import get_logger
from typing import Optional

class Speech:
    def __init__(self):
        self.settings: Settings = get_settings()
        self.logger = get_logger(__name__)

    def text_to_speech(self, text: str, output_file: str) -> bool: 
        """Converts text to speech and saves the audio to a file using Azure Cognitive Services.

    Args:
        text (str): The text to be converted to speech.
        output_file (str): The file path where the synthesized audio will be saved.

    Returns:
        bool: True if the text-to-speech conversion is successful.
        """
        # Configurate Speech Service
        speech_config = speechsdk.SpeechConfig(subscription= self.settings.speech_api_key,
                                            region= self.settings.speech_api_region)
        speech_config.speech_synthesis_voice_name='es-MX-GerardoNeural'

        # Configurate audio output to a file
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
        
        # Create an speech synthesizer object
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Sinthesize texto to speech
        result = speech_synthesizer.speak_text_async(text).get()

        # Handle result
        success = False
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            success = True
            self.logger.info(f"La síntesis de voz se completó correctamente y se guardó en {output_file}.")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            self.logger.warning(f"La síntesis de voz fue cancelada: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                self.logger.error(f"Error details: {cancellation_details.error_details}")

        return success
    
    def audio_to_text(self, audio_file_path: str) -> Optional[str]:
        """Converts an audio file to text using Azure Cognitive Services.

    Args:
        audio_file_path (str): The file path of the audio file to be transcribed.

    Returns:
        Optional[str]: The transcribed text if the transcription is successful.
        """
        try:
            # Configurar el objeto de configuración del reconocimiento de voz
            speech_config = speechsdk.SpeechConfig(subscription=self.settings.speech_api_key,
                                                region=self.settings.speech_api_region,
                                                speech_recognition_language="es-MX")
            audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)

            # Crear el objeto de reconocimiento de voz
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

            # Iniciar el reconocimiento de voz
            self.logger.info("Transcribing audio...")
            result = speech_recognizer.recognize_once()

            # Variable para almacenar el texto transcrito
            transcribed_text = ""

            # Manejar el resultado de la transcripción
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                transcribed_text = result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized")
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print(f"Speech Recognition canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print(f"Error details: {cancellation_details.error_details}")

            return transcribed_text
        except Exception as e:
            print(f'Error using audio_to_text. Error description: {str(e)}')
            return None