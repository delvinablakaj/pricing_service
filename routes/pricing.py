from models.models import PricingRequest,RequestPricing
from utils import get_listing_request,calculate_items_prices
from fastapi import (
    APIRouter,
    status)


router = APIRouter(tags=["Listings"])


@router.post("/request_price", status_code=status.HTTP_201_CREATED)
def post_calculate_pricing(body: RequestPricing):
    listing_request = body.dict()
    try:
        return calculate_items_prices(listing_request)
    except Exception as e:
        message = f"Error while pricing items: {e}"
        return message



