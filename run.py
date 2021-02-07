
# Check python version
import sys
if sys.version_info < (3,6):
    print('Python 3.6 or later is required')
    sys.exit(0)

# Gather args
args = sys.argv[1:]
if 'help' in args:
    print('Usage: run.py <option>')
    print(' refresh - Forces trade history update')
    print(' quiet - Do not print verbose data')
    print(' profit - Prints total profit, great for saving to database')
    print(' balance - Prints only total balance')
    sys.exit(0)
force_refresh = 'refresh' in args
print_profit_only = 'profit' in args
print_balance_only = 'balance' in args
quiet = 'quiet' in args

# Get data
from data import KrakenData
kraken_data = KrakenData(quiet=quiet)
kraken_data.loadTrades(force_refresh=force_refresh)
kraken_data.processTrades()
kraken_data.loadCurrentPrices()
data = kraken_data.calculateData()

# Print only profit
if print_profit_only:
    print(data['total_live_profit']+data['total_closed_profit'])
    sys.exit(0)
if print_balance_only:
    print(data['total_balance_usd'])
    sys.exit(0)

# Display
from utils import colorizeValue, printRow, Bold, Cyan
print('')
printRow('asset', 'live profit', 'closed profit', 'avg price', 'balance', color=Bold)
for asset in data['assets']:
    asset_str = str(asset['asset'])
    live_profit_str = colorizeValue(asset['live_profit_usd'], suffix='USD')
    closed_profit_str = colorizeValue(asset['closed_profit_usd'], suffix='USD')
    avg_price_usd = str(round(asset['average_price_usd'], 2))
    balance_str = str(round(asset['balance'], 5))
    printRow(asset_str, live_profit_str, closed_profit_str, avg_price_usd, balance_str)

total_live_profit_str = colorizeValue(data['total_live_profit'], suffix='USD', positiveColor=Cyan)
total_closed_profit_str = colorizeValue(data['total_closed_profit'], suffix='USD', positiveColor=Cyan)
printRow((Bold, 'TOTAL'), total_live_profit_str, total_closed_profit_str)

print('')
print('Total profit'.ljust(15), round(data['total_live_profit']+data['total_closed_profit'], 2))
print('End balance'.ljust(15), round(data['total_balance_usd'], 2))
print('')
