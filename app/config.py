from pydantic_settings import BaseSettings
from pydantic import Field, AliasChoices

class Settings(BaseSettings):
    mongodb_uri: str = Field(
        validation_alias=AliasChoices("MONGODB_URI", "MONGO_URI")
    )
    database_name: str = Field(
        default="hrms_lite",
        validation_alias=AliasChoices("DATABASE_NAME", "DB_NAME"),
    )

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
