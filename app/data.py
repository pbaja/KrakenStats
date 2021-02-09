from kraken import Kraken
from kraken.enums import KrakenOrderType

EPSILON = 0.000000000001

class KrakenData:

    def __init__(self, keys_file=None, quiet=False):
        # Create handle
        self.kraken = Kraken(keys_file='keys.json' if keys_file is None else keys_file)
        self.quiet = quiet

    def loadTrades(self, force_refresh=False, trades_file=None):
        # Load trades from file / download from API
        if trades_file is None: 'trades.json'
        self.trades, fresh = self.kraken.load_trades(trades_file, refresh_interval=0 if force_refresh else 60*60*6)
        if not self.quiet: print(f'Loaded {len(self.trades)} trades', '' if fresh else '(cached)')
        # Order them by time
        self.trades = sorted(self.trades, key=lambda trade: trade.time)

    def loadCurrentPrices(self):
        pairs = [f"{asset}USD" for asset in self.assets.keys() if asset != 'USD']
        tickers = self.kraken.get_tickers(pairs)
        self.current_prices = {'USD': 1.0}
        for ticker in tickers:
            self.current_prices[ticker.split_pair()[0]] = ticker.ask_price
        if not self.quiet: print('Loaded current prices')

    def processTrades(self):
        self.assets = {}
        for trade in self.trades:
            # Split pair into two assets
            a, b = trade.split_pair()
            if not a in self.assets: self.assets[a] = {'total_paid': 0.0, 'total_balance': 0.0, 'sell_profit': 0.0}
            #if not b in self.assets: self.assets[b] = {'total_paid': 0.0, 'total_balance': 0.0, 'sell_profit': 0.0}

            # How much we paid in USD
            cost_usd = 0.0
            if b == 'USD': cost_usd += trade.cost
            elif b == 'EUR': cost_usd += trade.cost * 1.2 # TODO: Calculate this accurately
            else: print(f'Unsupported currency: {b}');continue
            
            # Amount we bought/sold
            amount = trade.cost / trade.price

            # Bought some crypto
            if trade.type == KrakenOrderType.BUY:
                self.assets[a]['total_paid'] += cost_usd # How much we paid
                self.assets[a]['total_balance'] += amount # How much we got
            # Sold some
            elif trade.type == KrakenOrderType.SELL:
                if self.assets[a]['total_balance'] > EPSILON:
                    # Subtract from current balance keeping average in tact
                    curr_avg_price_usd = self.assets[a]['total_paid'] / self.assets[a]['total_balance']
                    self.assets[a]['total_paid'] -= curr_avg_price_usd * amount
                    self.assets[a]['total_balance'] -= amount
                    # Calculate profit we got from this sell
                    profit = cost_usd - curr_avg_price_usd * amount
                    self.assets[a]['sell_profit'] += profit
                else:
                    # Bought something with deposited money
                    pass

        for asset, price in self.assets.items():
            if price['total_balance'] < EPSILON: 
                self.assets[asset]['average_price'] = None
            else:
                average_price = price['total_paid'] / price['total_balance']
                self.assets[asset]['average_price'] = average_price

    def calculateData(self):
        data = {'total_balance_usd': 0.0, 'total_live_profit': 0.0, 'total_closed_profit': 0.0, 'avg_live_profit_percentage': 0.0, 'assets': []}
        for asset in self.assets.keys():
            if self.assets[asset]['average_price'] is None: 
                continue

            # Get current balance
            balance = self.assets[asset]['total_balance']
            if asset in self.current_prices:
                data['total_balance_usd'] += balance * self.current_prices[asset]

            # Profit
            closed_profit = self.assets[asset]['sell_profit']
            data['total_closed_profit'] += closed_profit
            live_profit = (self.current_prices[asset] - self.assets[asset]['average_price']) * balance if balance > EPSILON else 0.0
            data['total_live_profit'] += live_profit

            # Append to data
            live_profit_percentage = (self.current_prices[asset] / self.assets[asset]['average_price'] * 100.0) - 100.0
            data['assets'].append({
                'asset': asset,
                'live_profit_percentage': live_profit_percentage,
                'live_profit_usd': live_profit,
                'average_price_usd': self.assets[asset]['average_price'],
                'closed_profit_usd': closed_profit,
                'balance': balance
            })

            data['avg_live_profit_percentage'] += live_profit_percentage
        data['avg_live_profit_percentage'] /= len(data['assets'])
        return data