from optparse import Option
from unicodedata import name
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    lastname: str
    age:int
    phone_number: int
    password: str
    
class UserLogin(BaseModel):
    email: str
    password: str