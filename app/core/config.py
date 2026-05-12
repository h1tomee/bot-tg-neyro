from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    api_key: SecretStr
    model_name: str = "models/gemini-2.5-flash"
    
    model_config= SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    
settings = Settings()