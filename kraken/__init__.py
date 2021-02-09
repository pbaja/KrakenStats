import os, requests, time, hmac, hashlib, base64, urllib, json
from typing import List, Tuple
from enum import Enum
from pathlib import Path

from .objects import KrakenTrade, KrakenTicker
from .errors import KrakenError, KrakenErrorResponse, KrakenErrorHttp
from .enums import KrakenTradeType


class Kraken:

    def __init__(self, keys_file=None, api_key=None, private_key=None, base_url=None):
        # Get base url
        self.base_url = "https://api.kraken.com" if base_url is None else base_url
        # Get keys_file
        if keys_file is not None:
            if os.path.isfile(keys_file):
                with open(keys_file, "r") as f:
                    data = json.load(f)
                    self.api_key = data["api_key"]
                    self.private_key = data["private_key"]
            else:
                raise KrakenError(f'Please create {keys_file} with api_key and private_key. This is required to use Kraken API.')
        elif api_key is not None and private_key is not None:
            self.api_key = api_key
            self.private_key = private_key
        else:
            raise KrakenError('No keys_file or private_key and api_key supplied')

    def request_data(self, path, custom_data=None):

        # Data
        data = {'nonce': str(int(time.time()*1000))}
        if custom_data is not None: data.update(custom_data)

        # Signature generation and headers
        encoded = (data['nonce']+urllib.parse.urlencode(data)).encode()
        message = path.encode() + hashlib.sha256(encoded).digest()
        signature = hmac.new(base64.b64decode(self.private_key), message, hashlib.sha512)
        signature_digest = base64.b64encode(signature.digest())
        headers = {'API-Key': self.api_key, 'API-Sign': signature_digest.decode()}

        # Request
        url = self.base_url + path
        response = requests.post(self.base_url+path, data=data, headers=headers)
        if response.status_code != 200:
            raise KrakenErrorHttp(f'Server returned HTTP error code: {response.status_code}', {response.status_code})
        return response.json()

    def load_trades(self, trades_file, refresh_interval=0) -> Tuple[List[KrakenTrade], bool]:
        # Load trades from file
        if trades_file is None: trades_file = 'trades.json'
        trades_file_path = Path(trades_file)
        if trades_file_path.is_file():
            # Check if file is outdated
            last_update_time = time.time() - trades_file_path.stat().st_mtime
            if last_update_time < refresh_interval:
                # Return trades loaded from file
                with open(trades_file, 'r') as f:
                    trades_dict = json.load(f)
                    trades = [KrakenTrade.from_json(trade) for trade in trades_dict]
                    return (trades, False)

        # Download all trades
        new_trades = []
        offset_idx = 0
        while True:
            # Get new trades, break if no more trades
            new_trades = self.get_trades(offset_idx=offset_idx)
            if len(new_trades) == 0: break
            # Save and continue
            offset_idx += len(new_trades)
            trades += new_trades

        # Save to file and return
        with open(trades_file, 'w+') as f:
            trades_dict = [trade.__dict__ for trade in trades]
            json.dump(trades_dict, f, indent=4)
        return (trades, True)

    def get_trades(self, trade_type:KrakenTradeType=None, position_trades:bool=None, start_time:int=None, end_time:int=None, offset_idx:int=None) -> List[KrakenTrade]:
        # Prepare data
        data = {}
        if trade_type is not None: data['type'] = str(trade_type)
        if position_trades is not None: data['trades'] = 'true' if position_trades else 'false'
        if start_time is not None: data['start'] = start_time
        if end_time is not None: data['end'] = end_time
        if offset_idx is not None: data['ofs'] = offset_idx

        # Request result
        response = self.request_data('/0/private/TradesHistory', data)
        if 'result' in response:
            result = response['result']
            return [KrakenTrade.from_api(key, value) for key, value in result['trades'].items()]
        elif 'error' in response and len(response['error']) > 0:
            raise KrakenErrorResponse('Server returned error.', response['error'])

        # Unexpected behaviour
        raise KrakenError('Unexpected error')

    def get_tickers(self, pairs) -> List[KrakenTicker]:
        # Prepare data
        data = {'pair': ",".join(pairs)}

        # Request result
        response = self.request_data("/0/public/Ticker", data)
        if 'result' in response:
            result = response['result']
            return [KrakenTicker.from_api(key, value) for key, value in result.items()]
        elif 'error' in response and len(response['error']) > 0:
            raise KrakenErrorResponse('Server returned error.', response['error'])

        # Unexpected behaviour
        raise KrakenError('Unexpected error')