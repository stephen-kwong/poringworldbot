import dataclasses
import typing
import urllib.parse

import aiohttp


@dataclasses.dataclass
class Item:
    id: int
    item_id: int
    icon: str
    name: str
    price: int
    stock: int
    json: dict

    @classmethod
    def from_json_dict(cls, json_dct: dict) -> 'Item':
        """Convert an object from poring worlds api response to an item."""
        return cls(
            id=json_dct['id'],
            item_id=json_dct['itemId'],
            icon=json_dct['icon'],
            name=json_dct['name'],
            price=json_dct['lastRecord']['price'],
            stock=json_dct['lastRecord']['stock'],
            json=json_dct,
        )

    @property
    def icon_url(self):
        """The url to the icon of this item."""
        return f"https://www.poring.world/sprites/{self.icon}.png"


async def get(
        query: typing.Optional[str] = None,
        order: typing.Optional[str] = None,
        in_stock: typing.Optional[int] = None,
        modified: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
) -> typing.List[Item]:
    """
    Make a query to poring world's API.

    :param query: String to search the API for.
    :param order: How to order search results. Defaults to 'popularity'
    :param in_stock: 1 for in stock items only. 0 for out of stock. None for both.
    :param modified: 1 for items that have been refined/enchanted. 0 for not refined/enchanted. None for both.
    :param limit: Limit the number of results.
    :return: The results from poring world converted to Items
    """
    url = 'https://poring.world/api/search'
    params = dict(
        order=order or 'popularity',
        inStock=in_stock if in_stock is not None else '',
        modified=modified if modified is not None else '',
    )
    if query:
        params['q'] = query

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}?{urllib.parse.urlencode(params)}") as resp:
            content = await resp.json()

            if not limit:
                return [Item.from_json_dict(item) for item in content]
            else:
                return [Item.from_json_dict(item) for item in content[:limit]]
