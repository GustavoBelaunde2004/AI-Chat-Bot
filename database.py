from sqlalchemy import create_engine, Column, Integer, String, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from config import Settings, get_settings
from logger import get_logger
import pypyodbc
import aioodbc

class Database:
    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger(__name__)
        self.connection_string = "DRIVER={ODBC Driver 18 for SQL Server};SERVER="+self.settings.sql_server+";DATABASE="+self.settings.sql_database+";ENCRYPT=yes;UID="+self.settings.sql_username+";PWD="+self.settings.sql_password

    async def save_id_time_preference_to_db(self, user_id: str, timestamp, preference: str):
        async with aioodbc.create_pool(dsn=self.connection_string) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    try:                    
                        # Insertar datos
                        insert_query = f"""
                        INSERT INTO datos_preferencias_mensajes (user_id, timestamp, preference) 
                        VALUES (?, ?, ?)
                        """

                        data = [
                            (user_id, timestamp, preference),
                        ]
                        
                        for info in data:
                            await cursor.execute(insert_query, info)
                        
                        await conn.commit()
                        print(f"Datos insertados en la tabla datos_preferencias_mensajes exitosamente.")

                    except pypyodbc.DatabaseError as e:
                        print(f'Error en la base de datos: {e}')
                    finally:
                        await conn.rollback()

    async def get_user_info(self, user_id: str) -> bool:
        async with aioodbc.create_pool(dsn=self.connection_string) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    try:
                        query = f"SELECT timestamp, preference FROM datos_preferencias_mensajes WHERE user_id = ?"
                        await cursor.execute(query, [user_id])
                        result = await cursor.fetchone()
                        if result:
                            timestamp, preference = result
                            return timestamp, preference
                        else:
                            return False
                    except Exception as e:
                        self.logger.info(f'Error retrieving user info from table: {e}')
                        return None, None
    
    async def update_timestamp_and_preference(self, user_id: str, timestamp, preference: str):
        async with aioodbc.create_pool(dsn=self.connection_string) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    try:
                        update_query = """
                            UPDATE datos_preferencias_mensajes
                            SET timestamp = ?, preference = ?
                            WHERE user_id = ?
                        """
                        await cursor.execute(update_query, (timestamp, preference, user_id))
                        await conn.commit()
                        print(f"Datos actualizados en la tabla datos_preferencias_mensajes para el usuario {user_id}.")

                    except pypyodbc.DatabaseError as e:
                        print(f'Error en la base de datos: {e}')
                        await conn.rollback()


    