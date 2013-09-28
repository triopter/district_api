"""
.. module:: api
   :synopsis: This is the actual API client, along with a few helper classes.

.. moduleauthor:: Noemi Millman <noemi@triopter.com>
"""

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
    

class District(object):
    """
    Represents a district
    
    :ivar string district: The name or number of the district
    :ivar string level: Which political body this district elects to (e.g. 
       "City Council", "State Senate")
    :ivar string kml_url: URL to retrieve KML file representing the district's
       boundaries
    """

    def __init__(self, district, level, kml_url, *args, **kwargs):
        """
        :param string district: The name or number of the district
        :param string level: Which political body this district elects to (e.g. 
           "City Council", "State Senate")
        :param string kml_url: URL to retrieve KML file representing the district's
           boundaries
        """
        self.district = district
        self.level = level
        self.kml_url = kml_url
        
        super(District, self).__init__(*args, **kwargs)
    

class DistrictApi(object):
    """
    NY Times Districts API client.
    """
    def __init__(self, api_key, *args, **kwargs):
        """
        :param string api_key: NY Times Districts API key. Obtained from 
           `NY Times Developer Network <http://developer.nytimes.com/apps/register/>`_
        """
        super(DistrictApi, self).__init__(*args, **kwargs)
        
    def get_districts(self, lat_lng):
        """
        :param lat_lng: 2-tuple of latitude and longitude floats representing 
           the location for which district data should be retrieved -- e.g. 
           (34.6405, -85.3)
        :type lat_lng: tuple of floats
        :returns: Dictionary of District objects, indexed by level
        :rtype: dict
        """
        # Validate arguments
        # Construct request
        # Submit request
        # Parse response into dict
        # Validate response
        # Convert returned data into Python objects
        return {}
        
        