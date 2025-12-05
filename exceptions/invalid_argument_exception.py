class InvalidArgumentException(Exception):
    """Exception raised when there is a conflict with existing resources."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)