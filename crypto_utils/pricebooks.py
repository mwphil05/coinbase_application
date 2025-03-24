from typing import List
from typing import Any
from dataclasses import dataclass


@dataclass
class Ask:
    price: str
    size: str

    @staticmethod
    def from_dict(obj: Any) -> 'Ask':
        _price = str(obj.get("price"))
        _size = str(obj.get("size"))
        return Ask(_price, _size)


@dataclass
class Bid:
    price: str
    size: str

    @staticmethod
    def from_dict(obj: Any) -> 'Bid':
        _price = str(obj.get("price"))
        _size = str(obj.get("size"))
        return Bid(_price, _size)


@dataclass
class Pricebook:
    product_id: str
    bids: List[Bid]
    asks: List[Ask]
    time: str

    @staticmethod
    def from_dict(obj: Any) -> 'Pricebook':
        _product_id = str(obj.get("product_id"))
        _bids = [Bid.from_dict(y) for y in obj.get("bids")]
        _asks = [Ask.from_dict(y) for y in obj.get("asks")]
        _time = str(obj.get("time"))
        return Pricebook(_product_id, _bids, _asks, _time)


@dataclass
class Root:
    pricebooks: List[Pricebook]

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _pricebooks = [Pricebook.from_dict(y) for y in obj.get("pricebooks")]
        return Root(_pricebooks)
