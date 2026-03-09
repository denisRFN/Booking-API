from pydantic import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/desk_booking"

    class Config:
        env_file = ".env"


settings = Settings()
