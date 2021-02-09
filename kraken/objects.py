from .enums import KrakenOrderType
from .utils import clean_asset_name, split_pair

class KrakenTrade:
    @classmethod
    def from_api(cls, key_name, data):
        instance = cls()
        instance.id = key_name
        instance.ordertxid = data['ordertxid'] # Order responsible for execution of trade
        instance.postxid = data['postxid'] # ???
        instance.pair = data['pair'] # Asset pair
        instance.time = float(data['time']) # Unix timestamp of trade
        instance.type = KrakenOrderType(data['type']) # Type of order (buy/sell)
        instance.price = float(data['price']) # Average price order was executed at
        instance.cost = float(data['cost']) # Total cost of order (quote currency)
        instance.fee = float(data['fee']) # Total fee (quote currency)
        instance.volume = float(data['vol']) # Volume (base currency)
        instance.margin = float(data['margin']) # initial margin (quote currency)
        instance.misc = data['misc'].split(',') # List of miscellaneous info (most often empty)
        return instance

    @classmethod
    def from_json(cls, json_data):
        instance = cls()
        for key, value in json_data.items():
            if key == 'type': setattr(instance, key, KrakenOrderType(value))
            else: setattr(instance, key, value)
        return instance

    def split_pair(self):
        return split_pair(self.pair)

    @property
    def amount(self):
        return self.volume

class KrakenTicker:

    @classmethod
    def from_api(cls, key_name, data):
        instance = cls()
        instance.pair = key_name
        instance.ask_price = float(data['a'][0]) # price, whole lot volume, lot volume
        instance.bid_price = float(data['b'][0]) # price, whole lot volume, lot volume
        instance.last_price = float(data['c'][0]) # price, lot volume
        instance.volume_today = float(data['v'][0])
        instance.volume_24h = float(data['v'][1])
        instance.average_price_today = float(data['p'][0])
        instance.average_price_24h = float(data['p'][1])
        instance.trades_today = float(data['t'][0])
        instance.trades_24h = float(data['t'][1])
        instance.low_today = float(data['l'][0])
        instance.low_24h = float(data['l'][1])
        instance.high_today = float(data['h'][0])
        instance.high_24h = float(data['h'][1])
        instance.open_price = float(data['o'])
        return instance

    def split_pair(self):
        return split_pair(self.pair)