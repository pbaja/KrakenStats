import sys
from kraken import Kraken
from kraken.enums import KrakenOrderType
from utils import prettyFormat, printTable
from utils import Bold, Underline, Reset, Cyan

EPSILON = 0.000000000001
args = sys.argv[1:]
if 'help' in args:
    print('Usage: run.py <refresh/hide>')
    sys.exit(0)
force_refresh = 'refresh' in args
hide_amounts = 'hide' in args

# Get trades
kraken = Kraken(keys_file='keys.json')
trades = kraken.load_trades('trades.json', refresh_interval=0 if force_refresh else 60*60*6)
trades = sorted(trades, key=lambda trade: trade.time)

# Calculate total price and cost for each asset
price_count = {}
for trade in trades:
    # Split pair into two assets
    a, b = trade.split_pair()
    if not a in price_count: price_count[a] = {'total_paid': 0.0, 'total_balance': 0.0, 'sell_profit': 0.0}

    # How much we paid in USD
    cost_usd = 0.0
    if b == 'USD': cost_usd += trade.cost
    elif b == 'EUR': cost_usd += trade.cost * 1.2 # TODO: Calculate this accurately
    else: print(f'Unsupported currency: {b}');continue
    # Amount we bought/sold
    amount = trade.cost / trade.price

    # Bought some crypto
    if trade.type == KrakenOrderType.BUY:
        price_count[a]['total_paid'] += cost_usd # How much we paid
        price_count[a]['total_balance'] += amount # How much we got
    # Sold some crypto
    elif trade.type == KrakenOrderType.SELL and price_count[a]['total_balance'] > EPSILON:
        # Subtract from current balance keeping average in tact
        curr_avg_price_usd = price_count[a]['total_paid'] / price_count[a]['total_balance']
        price_count[a]['total_paid'] -= curr_avg_price_usd * amount
        price_count[a]['total_balance'] -= amount
        # Calculate profit we got from this sell
        profit = cost_usd - curr_avg_price_usd * amount
        price_count[a]['sell_profit'] += profit

# Calculate average
average_prices = {}
for asset, price in price_count.items():
    if price['total_balance'] < EPSILON: continue 
    average_price = price['total_paid'] / price['total_balance']
    average_prices[asset] = average_price

# # Get current prices
pairs = [f"{asset}USD" for asset in average_prices.keys() if asset != 'USD']
tickers = kraken.get_tickers(pairs)
print(f'Got {len(pairs)} tickers')
current_prices = {}
for ticker in tickers:
    current_prices[ticker.split_pair()[0]] = ticker.ask_price
print('')

# Calculate profit and loss
print(Bold+' '+'asset'.ljust(6), 'live profit'.ljust(14), 'closed profit'.ljust(14), 'balance'+Reset)
assets = price_count.keys()
total_live_profit = 0.0
total_closed_profit = 0.0
avg_percentage = [0.0, 0]
for asset in assets:
    # Get current balance
    balance = price_count[asset]['total_balance']

    # Live profit
    if balance > EPSILON:
        # Percentage
        live_profit_percentage = (current_prices[asset] / average_prices[asset] * 100.0) - 100.0
        avg_percentage[0] += live_profit_percentage
        avg_percentage[1] += 1
        live_profit_percentage_str = prettyFormat(live_profit_percentage, suffix='%', minlen=14)
        # USD
        live_profit = (current_prices[asset] - average_prices[asset]) * balance
        total_live_profit += live_profit
        live_profit_str = prettyFormat(live_profit, suffix='USD', minlen=14)
        # Balance
        balance_str = f'{round(balance,5)}'
    else:
        live_profit_percentage_str = '•'.ljust(14)
        live_profit_str = '•'.ljust(14)
        balance_str = '0.000'
    
    # Closed profit
    closed_profit = price_count[asset]['sell_profit']
    if closed_profit > EPSILON:
        total_closed_profit += closed_profit
        closed_profit_str = prettyFormat(closed_profit, suffix='USD', minlen=14)
    else:
        closed_profit_str = '•'.ljust(14)

    # Hide amounts
    if hide_amounts:
        live_profit_str = live_profit_percentage_str

    # Print
    print(' '+asset.ljust(6), live_profit_str, closed_profit_str, balance_str+Reset)

# Total
total_live_profit_percentage = avg_percentage[0] / avg_percentage[1]
total_live_profit_percentage_str = prettyFormat(total_live_profit_percentage, suffix='%', minlen=14, positiveColor=Cyan)
total_live_profit_str = prettyFormat(total_live_profit, suffix='USD', minlen=14, positiveColor=Cyan)
total_closed_profit_str = prettyFormat(total_closed_profit, suffix='USD', minlen=14, positiveColor=Cyan)
print('>'+'TOTAL'.ljust(6), total_live_profit_percentage_str if hide_amounts else total_live_profit_str, total_closed_profit_str, Reset)
print('')