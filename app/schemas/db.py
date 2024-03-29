from pydantic import BaseModel

class Database(BaseModel):
    db_driver: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str
    echo: bool = True
    future: bool = True