from fastapi import APIRouter

from controllers.mercadolibre import MercadoLibreController
from models.items import Item


router = APIRouter(
    prefix='/api',
    tags=['items']
)

RESULTS_PER_PAGE = 30

def paginate(items: list[Item], page: int) -> list[Item]:
    start = ( page - 1 ) * RESULTS_PER_PAGE
    end = page * RESULTS_PER_PAGE - 1
    return items[start:end]

@router.get('/search/')
@router.get('/search')
async def search(
    q: str,
    condition: str = '',
    price_order: int = 0,
    page: int = 1
):
    items: list[Item] = MercadoLibreController.search_items(q)
    if condition:
        items = list(filter(lambda item: item.condition == condition, items))
    if price_order:
        reversed = True if price_order > 0 else False
        items.sort(key=lambda item: item.price, reverse=reversed)
    return {
        'items': paginate(items, page),
        'total': len(items)
    }
