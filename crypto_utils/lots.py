"""
encapsulation of a Lot of crypto pairs
"""
from typing import Any
from dataclasses import dataclass


@dataclass
class Lot:
    """
    the Lot of crypto pairs
    """
    name: str
    quantity: str
    price_paid: str
    executed: bool
    value: str
    created_at: str

    @staticmethod
    def from_dict(obj: Any) -> 'Lot':
        """
        create the object from a dictionary
        :param obj:
        :return:
        """
        _name = str(obj.get("name"))
        _quantity = str(obj.get("quantity"))
        _price_paid = str(obj.get("price_paid"))
        _executed = bool(obj.get("executed"))
        _value = str(obj.get("value"))
        _created_at = str(obj.get("created_at"))
        return Lot(_name, _quantity, _price_paid, _executed, _value, _created_at)


# @dataclass
# class Root:
#     uuid: str
#     name: str
#     currency: str
#     available_balance: AvailableBalance
#     default: bool
#     active: bool
#     created_at: str
#     updated_at: str
#     deleted_at: str
#     type: str
#     ready: bool
#     hold: Hold
#     retail_portfolio_id: str
#     platform: str
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'Root':
#         _uuid = str(obj.get("uuid"))
#         _name = str(obj.get("name"))
#         _currency = str(obj.get("currency"))
#         _available_balance = AvailableBalance.from_dict(obj.get("available_balance"))
#         _default = ""
#         _active = ""
#         _created_at = str(obj.get("created_at"))
#         _updated_at = str(obj.get("updated_at"))
#         _deleted_at = str(obj.get("deleted_at"))
#         _type = str(obj.get("type"))
#         _ready = ""
#         _hold = Hold.from_dict(obj.get("hold"))
#         _retail_portfolio_id = str(obj.get("retail_portfolio_id"))
#         _platform = str(obj.get("platform"))
#         return Root(_uuid, _name, _currency, _available_balance, _default, _active,
#                     _created_at, _updated_at, _deleted_at, _type, _ready, _hold,
#                     _retail_portfolio_id, _platform)
