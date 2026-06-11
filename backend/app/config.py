from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Axon"
    debug: bool = True

    redis_url: str = "redis://localhost:6379/0"

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "axon_admin"
    minio_secret_key: str = "axon_secret"
    minio_bucket: str = "axon-datasets"
    minio_secure: bool = False

    mlflow_tracking_uri: str = "http://localhost:5000"

    class Config:
        env_file = ".env"


settings = Settings()