import requests

from models.items import Item


MERCADOLIBRE_ENDPOINT = 'https://api.mercadolibre.com/sites/MLA/search'

searches_cache: dict[str, list[Item]] = dict()

class MercadoLibreController(object):

    @classmethod
    def search_items(cls, q: str) -> list[Item]:
        if q in searches_cache:
            items = searches_cache[q]
        else:
            items = cls.request_mercadolibre_items(q)
            searches_cache[q] = items
        return items
    
    @classmethod
    def request_mercadolibre_items(cls, q: str) -> dict:
        query_params = {
            'q': q
        }
        json_response = requests.get(MERCADOLIBRE_ENDPOINT, params=query_params).json()
        items = cls.create_items_list(json_response)
        return items
    
    @classmethod
    def create_items_list(cls, json_data: dict) -> list[Item]:
        items = list()
        for item in json_data['results']:
            new_item = cls.create_new_item(item)
            items.append(new_item)
        return items
    
    @classmethod
    def create_new_item(cls, item_data: dict) -> Item:
        new_item = Item(
            id=item_data.get('id'),
            title=item_data.get('title'),
            price=item_data.get('price'),
            currency_id=item_data.get('currency_id'),
            available_quantity=item_data.get('available_quantity'),
            thumbnail=item_data.get('thumbnail'),
            condition=item_data.get('condition')
        )
        return new_item
