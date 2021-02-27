
def clean_asset_name(asset, is_fiat=None):
    if len(asset) == 4 and asset[0] == 'Z': asset = asset[1:]
    if asset == 'XXBT': return "BTC"
    if asset == 'XXMR': return "XMR"
    elif asset == 'XETH': return "ETH"
    elif asset == 'KUSD': return "USD"
    elif asset == 'MUSD': return "USD"
    elif asset == 'WUSD': return "USD"
    else: return asset

def split_pair(pair):
    left = round(len(pair) / 2)
    right = len(pair) - left
    return (clean_asset_name(pair[:left]), clean_asset_name(pair[-right:]))