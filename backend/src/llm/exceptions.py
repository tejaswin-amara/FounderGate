class ProviderError(Exception):
    pass

class RateLimitError(ProviderError):
    pass

class TimeoutError(ProviderError):
    pass

class AuthenticationError(ProviderError):
    pass

class ModelNotFoundError(ProviderError):
    pass
