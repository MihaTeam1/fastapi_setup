from pydantic import (
    BaseSettings,
)
from typing import List


class Settings(BaseSettings):
    allowed_hosts: List['str'] = ["127.0.0.1", "localhost"]
    origins: List['str'] = ["http://127.0.0.1", "http://localhost"]

    class Config:
        env_file = '.env/test'
