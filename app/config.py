from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    database_username: str
    database_name: str
    database_password: str
    database_port: str
    database_host: str
    secret_key: str
    algorithm: str
    expiry_time_taken: int 

    #for pydantiv before 2
    # class Config:
    #     env_file=".env"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

# @lru_cache()
# def get_Settings():
#     return Settings()