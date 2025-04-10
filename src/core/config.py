from typing import ClassVar, List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, Field


class Settings(BaseSettings):
    # Configuration de base
    PROJECT_NAME: str = "Aikunu API"
    ENVIRONMENT: str = "development"

    # Base de données
    DATABASE_URL: str = Field(
        default="sqlite:///./aikunu.db",
        description="URL de connexion à la base de données"
    )

    # Sécurité JWT
    SECRET_KEY: str = Field(
        default="change-me-in-production",
        min_length=32,
        description="Clé secrète pour les tokens JWT"
    )
    REFRESH_SECRET_KEY: str = Field(
        default="change-me-in-production-too",
        min_length=32,
        description="Clé secrète pour les refresh tokens"
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="Algorithme de chiffrement JWT"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=15,
        description="Durée de validité du token d'accès (en minutes)"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Durée de validité du refresh token (en jours)"
    )

    # Configuration optionnelle
    DEBUG: bool = Field(
        default=False,
        description="Mode debug (à désactiver en production)"
    )
    CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default=["http://localhost", "http://localhost:3000"],
        description="Origines autorisées pour CORS"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()