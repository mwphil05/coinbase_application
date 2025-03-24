from typing import Any
from dataclasses import dataclass


@dataclass
class AvailableBalance:
    value: str
    currency: str

    @staticmethod
    def from_dict(obj: Any) -> 'AvailableBalance':
        _value = str(obj.get("value"))
        _currency = str(obj.get("currency"))
        return AvailableBalance(_value, _currency)

@dataclass
class Hold:
    value: str
    currency: str

    @staticmethod
    def from_dict(obj: Any) -> 'Hold':
        _value = str(obj.get("value"))
        _currency = str(obj.get("currency"))
        return Hold(_value, _currency)

@dataclass
class Root:
    uuid: str
    name: str
    currency: str
    available_balance: AvailableBalance
    default: bool
    active: bool
    created_at: str
    updated_at: str
    deleted_at: str
    type: str
    ready: bool
    hold: Hold
    retail_portfolio_id: str
    platform: str

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _uuid = str(obj.get("uuid"))
        _name = str(obj.get("name"))
        _currency = str(obj.get("currency"))
        _available_balance = AvailableBalance.from_dict(obj.get("available_balance"))
        _default = ""
        _active = ""
        _created_at = str(obj.get("created_at"))
        _updated_at = str(obj.get("updated_at"))
        _deleted_at = str(obj.get("deleted_at"))
        _type = str(obj.get("type"))
        _ready = ""
        _hold = Hold.from_dict(obj.get("hold"))
        _retail_portfolio_id = str(obj.get("retail_portfolio_id"))
        _platform = str(obj.get("platform"))
        return Root(_uuid, _name, _currency, _available_balance, _default, _active,
                    _created_at, _updated_at, _deleted_at, _type, _ready, _hold,
                    _retail_portfolio_id, _platform)
