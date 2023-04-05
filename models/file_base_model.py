from pydantic import BaseModel
from fastapi import Form
from typing import Optional


class FileModel(BaseModel):
    file_name: str = Form(...)
    file_content: str = Form(...)
    category: int = Form(...)
    estafeta: int = Form(...)
    aprobado: Optional[int] = 0
