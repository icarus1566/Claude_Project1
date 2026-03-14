from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"  # env 파일에 정의되지 않은 변수가 있어도 에러 방지
    )

    PROJECT_NAME: str = "lfnovo On-prem RAG"
    API_V1_STR: str = "/api/v1"
    
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    LLM_MODEL: str = "llama3.1:8b"
    
    QDRANT_URL: str = "http://qdrant:6333"
    
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "documents"
    
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgrespassword"
    POSTGRES_DB: str = "rag_db"
    POSTGRES_SERVER: str = "postgresql"
    POSTGRES_PORT: int = 5432
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
