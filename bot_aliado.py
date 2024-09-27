from datetime import datetime
from config import Settings, get_settings
from logger import get_logger
from typing import Optional
import aiohttp

class BotAliado:
    def __init__(self):
        self.settings: Settings = get_settings()
        self.logger = get_logger(__name__)

    async def start_conversation(self, session:aiohttp.ClientSession) -> Optional[str]:
        """Starts a conversation using Bot Aliado API

        Args:
            session (aiohttp.ClientSession): Aiohttp session used by this conversation
            
        Returns:
            Optional[str]: The ID of the conversation
        """
        async with session.get(
            f'{self.settings.botaliado_api_url}/conversations/start/{self.settings.botaliado_user_id}', 
            headers={
                'accept': 'application/json',
                'x-api-key': self.settings.botaliado_api_key
            }
        ) as response:   
            if response.status == 200:
                data = await response.json()
                conversation_id = data['id']
                self.logger.info(f'Conversation started succesfully - id: {conversation_id}')
                return conversation_id
            else:
                self.logger.error(f'Error starting conversation')
                return None
            
    async def send_question(self, conversation_id: str, question:str, session:aiohttp.ClientSession) -> Optional[str]:
        """Sends a question to Bot Aliado API

        Args:
            conversation_id (str): The ID of the conversation where the question is going to be asked
            question (str): The text question that is going to be asked
            session (aiohttp.ClientSession): Aiohttp session used by this conversation

        Returns:
            Optional[str]: Retuns the response text of the question
        """
        async with session.post(
            f'{self.settings.botaliado_api_url}/conversations/ask', 
            headers={
                'accept': 'application/json',
                'x-api-key': self.settings.botaliado_api_key,
                'Content-Type': 'application/json'
            }, 
            json={
                'conversation_id': conversation_id,
                'user_id': self.settings.botaliado_user_id,
                'query': question
            }
        ) as response:
            if response.status == 200:
                data = await response.json()
                response_text = data['response']['content']
                return response_text
            else:
                self.logger.error('Error generating response.')
                return None
        
    def find_conversation_today(self, conversations: list[dict]) -> Optional[str]: 
        """  Finds the conversation that occurred today from a list of conversations.


    Args:
        conversations (list[dict]): A list of conversation dictionaries, where each
                                    dictionary contains the date of the last message.

    Returns:
        Optional[str]: The ID of the conversation that occurred today, or None.
        """
        today = datetime.now().strftime('%Y/%m/%d')
        for conversation in conversations:
            last_message_date = conversation['lastMessage']['date'].split(' ')[0]
            if last_message_date == today:
                return conversation['conversationId']
        return None
    
    async def get_conversation_history(self, session:aiohttp.ClientSession) -> Optional[str]: #FALTA DOCUMENTAR
        """    Fetches the conversation history for the user from the BotAliado API.

    Args:
        session (aiohttp.ClientSession): Aiohttp session used to make the HTTP request.

    Returns:
        Optional[str]: The ID of the conversation if found, otherwise None.
        """
        async with session.get(
            f'{self.settings.botaliado_api_url}/conversations/user/{self.settings.botaliado_user_id}', 
            headers={
                'accept': 'application/json',
                'x-api-key': self.settings.botaliado_api_key
            }
        ) as response:
            if response.status == 200:
                data = await response.json()
                conversation_id = self.find_conversation_today(data)
                return conversation_id
            else:
                self.logger.error(f'Error getting conversation history')
                return None
                
