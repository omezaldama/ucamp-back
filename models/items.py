from pydantic import BaseModel

class Item(BaseModel):
    id: str
    title: str
    price: float
    currency_id: str
    available_quantity: int
    thumbnail: str
    condition: str
