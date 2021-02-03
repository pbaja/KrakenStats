
class KrakenError(Exception):
    pass

class KrakenErrorResponse(Exception):
    def __init__(self, message, data):
        super().__init__(self, message)
        print(data.keys())