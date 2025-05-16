from pydantic import BaseSettings

class Settings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    database_url: str
    secret_key: str
    invite_code_length: int = 8
    cluster_default_resources: dict = {
        "cpu": 4,
        "ram": "16Gi",
        "gpu": 1
    }

    class Config:
        env_file = ".env"

settings = Settings()