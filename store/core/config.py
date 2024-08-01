from pydantic_settings import BaseSettings, SettingsConfigDict

<<<<<<< HEAD

class Settings(BaseSettings):
    PROJECT_NAME: str = "Store API"
    ROOT_PATH: str = "/"

    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
=======
class Settings(BaseSettings):
    PROJECT_NAME: str = "Store API"
    ROOT_PATH: str = "/"
    
    DATABASE_URL: str 
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()
>>>>>>> f44af51a971f61c5e771acb97d8ff8fdabaf3363
