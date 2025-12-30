from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    #Configs cargadas desde env
    
    # DB
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # User
    INITIAL_USER_EMAIL: str
    INITIAL_USER_PASSWORD: str
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Task Management API"
    
    # Configuración para cargar desde .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property #Pasa a atributo la funcion
    def DATABASE_URL(self) -> str:
        #Construcción de URL
        url = f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return url


@lru_cache()#Last Reciently used cache
def get_settings() -> Settings:
    """Obtener configuración (cached)"""
    return Settings()
