# c3po exception


# Create translation registration execptions
class AlreadyRegistered(Exception):
    """
        Raised when you try and register a
        model for translation more than once
    """
    pass
