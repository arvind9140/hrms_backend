from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "hrms_lite"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
