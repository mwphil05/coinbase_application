from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Maintenance:
    start_time: str
    end_time: str

    @staticmethod
    def from_dict(obj: Any) -> 'Maintenance':
        _start_time = str(obj.get("start_time"))
        _end_time = str(obj.get("end_time"))
        return Maintenance(_start_time, _end_time)

@dataclass
class PerpetualDetails:
    open_interest: str
    funding_rate: str
    funding_time: str
    max_leverage: str
    base_asset_uuid: str
    underlying_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'PerpetualDetails':
        _open_interest = str(obj.get("open_interest"))
        _funding_rate = str(obj.get("funding_rate"))
        _funding_time = str(obj.get("funding_time"))
        _max_leverage = str(obj.get("max_leverage"))
        _base_asset_uuid = str(obj.get("base_asset_uuid"))
        _underlying_type = str(obj.get("underlying_type"))
        return PerpetualDetails(_open_interest, _funding_rate, _funding_time, _max_leverage, _base_asset_uuid, _underlying_type)

@dataclass
class FcmTradingSessionDetails:
    is_session_open: str
    open_time: str
    close_time: str
    session_state: str
    after_hours_order_entry_disabled: str
    closed_reason: str
    maintenance: Maintenance

    @staticmethod
    def from_dict(obj: Any) -> 'FcmTradingSessionDetails':
        _is_session_open = str(obj.get("is_session_open"))
        _open_time = str(obj.get("open_time"))
        _close_time = str(obj.get("close_time"))
        _session_state = str(obj.get("session_state"))
        _after_hours_order_entry_disabled = str(obj.get("after_hours_order_entry_disabled"))
        _closed_reason = str(obj.get("closed_reason"))
        _maintenance = Maintenance.from_dict(obj.get("maintenance"))
        return FcmTradingSessionDetails(_is_session_open, _open_time, _close_time, _session_state,
                                        _after_hours_order_entry_disabled, _closed_reason,
                                        _maintenance)

@dataclass
class FutureProductDetails:
    venue: str
    contract_code: str
    contract_expiry: str
    contract_size: str
    contract_root_unit: str
    group_description: str
    contract_expiry_timezone: str
    group_short_description: str
    risk_managed_by: str
    contract_expiry_type: str
    perpetual_details: PerpetualDetails
    contract_display_name: str
    time_to_expiry_ms: str
    non_crypto: str
    contract_expiry_name: str
    twenty_four_by_seven: str

    @staticmethod
    def from_dict(obj: Any) -> 'FutureProductDetails':
        _venue = str(obj.get("venue"))
        _contract_code = str(obj.get("contract_code"))
        _contract_expiry = str(obj.get("contract_expiry"))
        _contract_size = str(obj.get("contract_size"))
        _contract_root_unit = str(obj.get("contract_root_unit"))
        _group_description = str(obj.get("group_description"))
        _contract_expiry_timezone = str(obj.get("contract_expiry_timezone"))
        _group_short_description = str(obj.get("group_short_description"))
        _risk_managed_by = str(obj.get("risk_managed_by"))
        _contract_expiry_type = str(obj.get("contract_expiry_type"))
        _perpetual_details = PerpetualDetails.from_dict(obj.get("perpetual_details"))
        _contract_display_name = str(obj.get("contract_display_name"))
        _time_to_expiry_ms = str(obj.get("time_to_expiry_ms"))
        _non_crypto = str(obj.get("non_crypto"))
        _contract_expiry_name = str(obj.get("contract_expiry_name"))
        _twenty_four_by_seven = str(obj.get("twenty_four_by_seven"))
        return FutureProductDetails(_venue, _contract_code, _contract_expiry, _contract_size,
                                    _contract_root_unit, _group_description,
                                    _contract_expiry_timezone, _group_short_description,
                                    _risk_managed_by, _contract_expiry_type, _perpetual_details,
                                    _contract_display_name, _time_to_expiry_ms, _non_crypto,
                                    _contract_expiry_name, _twenty_four_by_seven)

@dataclass
class Root:
    product_id: str
    price: str
    price_percentage_change_24h: str
    volume_24h: str
    volume_percentage_change_24h: str
    base_increment: str
    quote_increment: str
    quote_min_size: str
    quote_max_size: str
    base_min_size: str
    base_max_size: str
    base_name: str
    quote_name: str
    watched: bool
    is_disabled: str
    new: bool
    status: str
    cancel_only: bool
    limit_only: bool
    post_only: bool
    trading_disabled: str
    auction_mode: bool
    product_type: str
    quote_currency_id: str
    base_currency_id: str
    mid_market_price: str
    alias: str
    alias_to: List[str]
    base_display_symbol: str
    quote_display_symbol: str
    view_only: bool
    price_increment: str
    display_name: str
    product_venue: str
    approximate_quote_24h_volume: str
    new_at: str

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _product_id = str(obj.get("product_id"))
        _price = str(obj.get("price"))
        _price_percentage_change_24h = str(obj.get("price_percentage_change_24h"))
        _volume_24h = str(obj.get("volume_24h"))
        _volume_percentage_change_24h = str(obj.get("volume_percentage_change_24h"))
        _base_increment = str(obj.get("base_increment"))
        _quote_increment = str(obj.get("quote_increment"))
        _quote_min_size = str(obj.get("quote_min_size"))
        _quote_max_size = str(obj.get("quote_max_size"))
        _base_min_size = str(obj.get("base_min_size"))
        _base_max_size = str(obj.get("base_max_size"))
        _base_name = str(obj.get("base_name"))
        _quote_name = str(obj.get("quote_name"))
        _watched = True
        _is_disabled = str(obj.get("is_disabled"))
        _new = True
        _status = str(obj.get("status"))
        _cancel_only = True
        _limit_only = True
        _post_only = True
        _trading_disabled = str(obj.get("trading_disabled"))
        _auction_mode = True
        _product_type = str(obj.get("product_type"))
        _quote_currency_id = str(obj.get("quote_currency_id"))
        _base_currency_id = str(obj.get("base_currency_id"))
        _mid_market_price = str(obj.get("mid_market_price"))
        _alias = str(obj.get("alias"))
        _alias_to = []
        _base_display_symbol = str(obj.get("base_display_symbol"))
        _quote_display_symbol = str(obj.get("quote_display_symbol"))
        _view_only = True
        _price_increment = str(obj.get("price_increment"))
        _display_name = str(obj.get("display_name"))
        _product_venue = str(obj.get("product_venue"))
        _approximate_quote_24h_volume = str(obj.get("approximate_quote_24h_volume"))
        _new_at = str(obj.get("new_at"))

        return Root(_product_id, _price, _price_percentage_change_24h, _volume_24h,
                    _volume_percentage_change_24h, _base_increment, _quote_increment,
                    _quote_min_size, _quote_max_size, _base_min_size, _base_max_size,
                    _base_name, _quote_name, _watched, _is_disabled, _new, _status, _cancel_only,
                    _limit_only, _post_only, _trading_disabled, _auction_mode, _product_type,
                    _quote_currency_id, _base_currency_id, _mid_market_price, _alias, _alias_to,
                    _base_display_symbol, _quote_display_symbol, _view_only, _price_increment,
                    _display_name, _product_venue, _approximate_quote_24h_volume, _new_at)
