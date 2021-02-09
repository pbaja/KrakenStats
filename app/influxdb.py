import time, json, os, sys

def run():
    # Grab info
    if os.path.isfile('influxdb.json'):
        with open('influxdb.json', "r") as f:
            config = json.load(f)
    else:
        raise Exception(f'Please create influxdb.json with fields: url,token,org,bucket and optionally: measurement,field')

    # Connect to a database
    try:
        from influxdb_client import InfluxDBClient
    except ImportError:
        print('No influxdb_client library. Install with "pip install influxdb_client"')
        sys.exit(0)
    influx = InfluxDBClient(url=config['url'], token=config['token'], org=config['org'])
    writer = influx.write_api()
    print('Connected to InfluxDB')

    # Get data
    from kraken.errors import KrakenErrorHttp
    from .data import KrakenData
    counter = 0
    failed_attempts = 0
    failed_attempts_wait = [2, 3, 5, 10]
    kraken_data = KrakenData(keys_file='keys.json', quiet=True)
    print('Initialized Kraken API')
    interval = config['interval'] if 'interval' in config else 60
    print(f'Insert every {interval} seconds')
    while True:
        # Refresh
        try:
            kraken_data.loadTrades(trades_file='trades.json')
            kraken_data.processTrades()
            kraken_data.loadCurrentPrices()
            data = kraken_data.calculateData()
            failed_attempts = 0
            counter += 1
        except KrakenErrorHttp as e:
            # Get wait time before next attempt
            wait_minutes = failed_attempts_wait[failed_attempts if failed_attempts < len(failed_attempts_wait) else len(failed_attempts_wait)-1]
            failed_attempts += 1
            print(f"\nKraken API server returned HTTP {e.code} error. Retrying in {wait_minutes} minutes (attempt {failed_attempts})")
            time.sleep(wait_minutes * 60)
            continue

        # Calculate profit
        profit = data['total_live_profit'] + data['total_closed_profit']

        # Push to database
        measurement = config['measurement'] if 'measurement' in config else 'kraken'
        field = config['field'] if 'field' in config else 'profit'
        writer.write(config['bucket'], config['org'], [f"{measurement} {field}={profit}"])
        
        # Progress
        if counter % 20 == 0: print('.')
        else: print(".", end='', flush=True)

        # Wait for 60 seconds
        time.sleep(interval)