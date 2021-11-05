from dataclasses import dataclass


@dataclass
class User:
    name: str
    phone: str
    email: str
    verified: bool = False
