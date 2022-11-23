from pydantic import BaseModel
from typing import Optional

class Queue(BaseModel):
    name: str
    info: list[float, int]