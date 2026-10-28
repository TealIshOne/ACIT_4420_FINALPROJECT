"""
error handelign and raised 'personalised' exceptions

"""

class BusBidderError(Exception):
    """parent of all BusBidder errors"""

class InvalidFileError(BusBidderError):
    def __init__(self, path, file_name):
        self.path=path
        self.file_name=file_name

        message=(
            f"fil '{path}'/'{file_name}' not found"
        )
        super().__init__(message)


class InvalidIdentifierError(BusBidderError):
    def __init__(self, identifier, id_type, expected_pattern):
        self.identifier = identifier
        self.id_type= id_type
        self.expected_pattern=expected_pattern
        message=(
            f"invalid '{id_type}': '{identifier}' "
            f"does not match expected patern {expected_pattern}"
        )
        super().__init__(message)

class InvalidOfferError(BusBidderError):
    """row has a bad value"""
    def __init__(self, offer_id, reason):
        self.offer_id=offer_id
        self.reason = reason
        message=(
            f"offer '{offer_id}' : {reason}"
        )
        super().__init__(message)

    

class BookingError(BusBidderError):
    '''
    trouble in booking, to few seats, etc
    '''
    pass

class WeightsError(BusBidderError):
    '''
    weights dont add up to 100
    '''
    pass