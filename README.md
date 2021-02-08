<p align="center">
<img align="center" src="preview.png">
</p>

## Warning
 - This tool is not very accurate, f.eg. it does not consider fees in calculations (work in progress)
 - It does not provide any professional capacity, do *not* use it for calculating taxes!
 - This tool only supports USD/EUR as a buying currency (work in progress)
 - Conversion from EUR to USD is not very accurate either (work in progress)
 - It does not work for positions, only buy/sell trades
  
## Features
 - Automatically downloads trade history from your Kraken account
 - Calculating open and closed profits/losses
 - Displaying them as percentages or USD amounts
  
## Usage
 - Download code
 - Generate API Key and Private Key by going to kraken.com -> your name -> Security -> API -> Add key. We only need one permission: `Query Ledger Entries`
 - Create `keys.json` file with just generated API Key and Private Key (see below for example file)
 - Run examples with command `python run.py stats` or see list of examples with `python run.py help`
  
### Example keys.json file
```
{ "api_key": "INSERT_API_KEY_HERE", "private_key": "INSERT_PRIV_KEY_HERE"}
```
  
### Example influxdb.json file
```
{
    "url": "http://INSERT_INFLUXDB_IP_HERE:INSERT_PORT_HERE", 
    "token": "INSERT_TOKEN_HERE",
    "org": "home",
    "bucket": "kraken",
    "measurement": "kraken",
    "field": "profit"
}
```