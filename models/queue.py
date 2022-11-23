from pydantic import BaseModel
from typing import Optional

class Queue(BaseModel):
    name: str
    data: list[float, int]