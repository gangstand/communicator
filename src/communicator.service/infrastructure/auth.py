from pydantic import Field
from pydantic_settings import BaseSettings

from domain.auth import EntityAuth


class AuthSettings(BaseSettings):
    authjwt_secret_key: str = Field(alias="SECRET")


class UtilsEntityAuth(EntityAuth):
    secret_key = AuthSettings().authjwt_secret_key
