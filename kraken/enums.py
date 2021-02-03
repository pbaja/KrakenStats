from enum import Enum

class KrakenTradeType(str, Enum):
    ALL              = 'all' # All types (default)
    ANY_POSITION     = 'any position' # Any position (open or closed)
    CLOSED_POSITION  = 'closed position' # Positions that have been closed
    CLOSING_POSITION = 'closing position' # Any trade closing all or part of a position
    NO_POSITION      = 'no position' # Non-positional trades

class KrakenOrderType(str, Enum):
    BUY  = 'buy'
    SELL = 'sell'
    