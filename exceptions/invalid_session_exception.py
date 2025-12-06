class InvalidSessionException(Exception):
    """Exception raised for invalid student sessions."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)