from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class Inventory(BaseModel):
    itemId: str = Field(...)
    condition: str = Field(...)
    category: str = Field(...)
    subcategory: Optional[str]
    material: str = Field(...)
    brand: str = Field(...)
    gender: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    size: str = Field(...)
    title: str = Field(...)
    color: str = Field(...)
    images: list = Field(...)
    temp_category: Optional[str]
    tier: Optional[str]
    created_at: Optional[datetime]


class RequestPricing(BaseModel):
    listingId: str
    status: Optional[str]
    margin: Optional[float]
    marketplace: str = Field(...)
    deleted: Optional[bool]
    inventory: List[Inventory] = Field(...)
    items: Optional[List[object]]
    createdAt: datetime = datetime.now()
    events: list = []

    class Config:
        arbitrary_types_allowed = True

