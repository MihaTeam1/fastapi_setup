from pydantic import (
    BaseSettings,
)
from typing import List


class Settings(BaseSettings):
    pass

    class Config:
        env_file = '.env/test'
