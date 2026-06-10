from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CreateProductDTO:
    name: str
    price: float

@dataclass
class CreateOrderDTO:
    items: List[str]

@dataclass
class RegisterUserDTO:
    username: str
    password: str
