
class DistrictApiError(Exception):
    """
    Parent class from which all other Districts API errors inherit.
    
    Used for any other generic exceptions.
    """
    pass

class ApiUnavailable(DistrictApiError):
    """
    Thrown when network or server errors are encountered.
    """
    pass
    
    
class LocationUnavailable(DistrictApiError):
    """
    As of this writing, the Times' Districts API only offers data for New York 
    City districts. This exception is thrown when the API returns a response
    indicating that the lat/long given are outside the area covered.       
    """
    pass
    
    
class AuthorizationError(DistrictApiError):
    """
    Receiving this error probably means your API key is invalid.
    """
    pass
    
    
class QuotaExceeded(DistrictApiError):
    """
    Currently unused (because we haven't hit our quota and thus haven't been 
    able to see what the API returns in this case!)
        
    When we do get this running, well, it'll mean you've exceeded your quota.
    """
    pass
    
    
class BadRequest(DistrictApiError):
    """
    Raised when server returns a 400 response.  It probably actually means we
    screwed up somewhere in the API client logic, but at least this way you can 
    catch it if you have to.
    """
    pass
    
class InvalidResponse(DistrictApiError):
    """
    Raised if dict parsed from JSON doesn't contain the keys / values expected.
    """
    pass   