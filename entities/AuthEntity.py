from pydantic import BaseModel

class AuthDetail(BaseModel):
    client_id: str
    client_secret: str

    