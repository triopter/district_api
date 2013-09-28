"""
.. module:: api
   :synopsis: This is the actual API client, along with a few helper classes.

.. moduleauthor:: Noemi Millman <noemi@triopter.com>
"""

import requests

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
    
    def __eq__(self, other):
        try:      
            return all((
                self.district == other.district,
                self.level == other.level,
                self.kml_url == other.kml_url,
            ))
        
        except AttributeError:
            return False
        
    def __lt__(self, other):
        # comparisons are different for numeric vs. non-numeric district names
        try:
            self_comp = int(self.district)
            other_comp = int(other.district)
            
        except ValueError:
            self_comp = self.district
            other_comp = other.district
            
        except AttributeError:
            raise TypeError('Cannot compare District object with object lacking '
                '"district" attribute')
        
        return self_comp < other_comp
        

class DistrictApi(object):
    """
    NY Times Districts API client.

    :ivar string api_key: NY Times Districts API key. Obtained from 
       `NY Times Developer Network <http://developer.nytimes.com/apps/register/>`_
    :ivar string url: Endpoint for NY Times Districts API.  Defaults to URL
        specified in `the docs <http://developer.nytimes.com/docs/districts_api>`_
    """
    def __init__(self, api_key, *args, **kwargs):
        """
        :param string api_key: NY Times Districts API key. Obtained from 
           `NY Times Developer Network <http://developer.nytimes.com/apps/register/>`_
        :param string url: Override API endpoint (used mostly for testing)
        """
        self.api_key = api_key
        self.url = kwargs.pop('url', 'http://api.nytimes.com/svc/politics/v2/districts.json')
        
        super(DistrictApi, self).__init__(*args, **kwargs)

    def construct_query_vars(self, lat_lng=None):
        """
        Constructs the query string for our particular API query.  Called by 
        ``send_request``.  This doesn't really need to be a separate method,
        but it makes for easier unit testing.
            
        :param lat_lng: 2-tuple of latitude and longitude floats representing 
           the location for which district data should be retrieved -- e.g. 
           (34.6405, -85.3).  If omitted, data for all available districts will 
           be returned.
           
        :type lat_lng: tuple of floats
        :returns: Dictionary of variables that should be included in the query 
           string when querying the API
           
        :rtype: dict
        """
        query_vars = {
            'api_key': self.api_key,
        }
        
        if lat_lng:
            query_vars['lat'] = lat_lng[0]
            query_vars['lng'] = lat_lng[1]
        
        return query_vars
        
    def send_request(self, lat_lng=None):
        """
        Construct query string; send HTTP request to API; return HTTP response.
        
        :param lat_lng: 2-tuple of latitude and longitude floats representing 
           the location for which district data should be retrieved -- e.g. 
           (34.6405, -85.3).  If omitted, data for all available districts will 
           be returned.
           
        :type lat_lng: tuple of floats
        :returns: raw HTTP response from API
        :rtype: requests.Response
        """
        query_vars = self.construct_query_vars(lat_lng)
        return requests.get(self.url, params=query_vars)
        
    def validate_response(self, response):
        """
        Handles cases where response status code is not 200, by raising custom
        exceptions.
        
        :param requests.Response response: Response object returned by Times API
        :raises: ApiUnavailable, AuthorizationError, BadRequest, DistrictApiError 
        """
        if response.status_code == 200:
            return
        
        if response.status_code == 400:
            raise BadRequest(response)
            
        if response.status_code in (404, 500):
            raise ApiUnavailable(response)
            
        if response.status_code == 403:
            raise AuthorizationError(response)
            
        # Unknown error status
        raise DistrictApiError(response)
        
    def parse_response(self, response):
        """
        Converts JSON from response body into a Python dict.
        
        :param requests.Response response: Response object returned by Times API
        :returns: Dictionary containing district information and metadata
        :rtype: dict
        """
        # the requests library will even parse JSON for us.  How easy is that?
        return response.json
    
    def validate_response_body(self, response_dict):
        """
        Handles cases where response status code is 200, but response body 
        indicates an error, by raising custom exceptions
        
        :param dict response_dict: Dictionary containing response data parsed
            from JSON returned by the Times API
            
        :raises: LocationUnavailable
        """
        status = response_dict.get('status')
        if status != 'OK':
            errs = response_dict.get('errors')
            raise LocationUnavailable(errs)
            
    def get_data(self, lat_lng=None):
        """
        Construct query string; send HTTP request to API; return HTTP response.
        
        :param lat_lng: *(optional)* 2-tuple of latitude and longitude floats 
            representing the location for which district data should be 
            retrieved -- e.g. (34.6405, -85.3).  If omitted, data for all 
            available districts will be returned.
           
        :type lat_lng: tuple of floats or None
        :returns: Dictionary of raw data parsed from JSON API response
        :rtype: dict
        """
        response = self.send_request((lat, lng,))
        
        # validate response status code
        self.validate_response(response)
        
        # Parse response into dict
        data = self.parse_response(response)
        
        # Validate response
        self.validate_response_body(data)
        
        
    def get_all_districts(self):
        """
        Get information about all districts about which the API can provide data.
        
        :raises: ApiUnavailable, AuthorizationError, BadRequest, 
            LocationUnavailable, DistrictApiError
            
        :returns: Dictionary containing a list of district objects for each 
            electoral level
            
        :rtype: dict
        """
        return {}
    
    def get_districts(self, lat_lng):
        """
        Get information about districts to which a given location belongs.
        
        Will throw uncaught TypeError if lat_lng is not iterable or ValueError 
        if lat or lng are not floats.
           
        If lat_lng contains more than 2 items, additional items will be ignored
        
        :param lat_lng: 2-tuple of latitude and longitude floats representing 
           the location for which district data should be retrieved -- e.g. 
           (34.6405, -85.3)
        :type lat_lng: tuple of floats
        :raises: TypeError, ValueError, ApiUnavailable, AuthorizationError, 
            BadRequest, LocationUnavailable, DistrictApiError
            
        :returns: Dictionary of District objects, indexed by level
        :rtype: dict
        """
        # Validate arguments
        lat = float(lat_lng[0])
        lng = float(lat_lng[1])
        
        data = self.get_data((lat, lng,))
        
        # Convert returned data into Python objects
        return {}
        
        