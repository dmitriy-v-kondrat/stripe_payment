

from pydantic import BaseModel

from tests.src.enums.item_enum import Currency


class ItemField(BaseModel):
    name: str
    description: str
    price: int
    currency: Currency
