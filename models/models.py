from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional,List


# class Item(BaseModel):
#     item_id: str = Field(...)


class PricingRequest(BaseModel):
    id: str
    listing_id = Optional[str]

    createdAt: datetime = datetime.now()

    class Config:
        arbitrary_types_allowed = True


class Item(BaseModel):
    brand: str
    brand_tier: str
    category: str
    color: str
    condition: str
    description:str
    gender: str
    images: List[str]
    item_id:str
    material: str
    price: float
    size: str
    title: str

class Credentials(BaseModel):
    username: str="test@yopmail.com"
    password: str= "123456"

class RequestPricing(BaseModel):
    marketplace: str
    listing_id: str
    margin: float=0.1
    credentials: Credentials
    items: List[Item]

    class Config:
        arbitrary_types_allowed = True
