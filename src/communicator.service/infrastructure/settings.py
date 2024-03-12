from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class DataBaseSettings(BaseSettings):
    host: str = Field(alias="DB_HOST")
    port: int = Field(alias="DB_PORT")
    name: str = Field(alias="DB_NAME")
    user: str = Field(alias="DB_USER")
    password: str = Field(alias="DB_PASS")


class PathSetting(BaseSettings):
    path: str = Field(alias="URL_PATH", default="http://127.0.0.1:9001/api-static")


SAVE_PATH = Path("static")
URL_PATH = Path(PathSetting().path)
ID_MANAGER = "19ce910d-069b-4a7f-9a2d-ccbcb2636a62"
