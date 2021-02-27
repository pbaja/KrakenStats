
class KrakenError(Exception):
	pass

class KrakenErrorHttp(KrakenError):
    def __init__(self, message, code):
    	super().__init__(self, message)
    	self.code = code

class KrakenErrorResponse(KrakenError):
    def __init__(self, message, data):
        super().__init__(self, message)
        print(data)