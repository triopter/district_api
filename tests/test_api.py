from unittest import TestCase
from requests import Request

from district_api.api import DistrictApi, District, DistrictApiError, \
    ApiUnavailable, LocationUnavailable, AuthorizationError, QuotaExceeded

class ApiTestCase(TestCase):
    api_key = 'dummy'

    def setUp(self):
        self.client = DistrictApi(self.api_key)
        
    def test_construction(self):
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client.url, 'http://api.nytimes.com/svc/politics/v2/districts.json')

        other_client = DistrictApi(self.api_key, url='http://www.example.com')
        self.assertEqual(other_client.url, 'http://www.example.com')

    def test_validation(self):    
        with self.assertRaises(TypeError):
            self.client.get_districts(12.3456, 10.432)
            
        with self.assertRaises(ValueError):
            self.client.get_districts(('a', 10.432))
            
        with self.assertRaises(ValueError):
            self.client.get_districts((10.432, 'a'))
            
        try:
            self.client.get_districts((12.3456, 10.432))
            self.client.get_districts((12.3456, -10.432))
            self.client.get_districts((12, 10))
            self.client.get_districts((12, -10))
            self.client.get_districts(('12.3456', '10.432'))
            self.client.get_districts(('12.3456', '-10.432'))
            self.client.get_districts(('12', '10'))
            self.client.get_districts(('12', '-10'))
        except (TypeError, ValueError):
            self.fail('get_districts should accept float, int, and strings that'
                'can be converted to floats/ints')
                
    def test_construct_query_vars(self):
        qv = self.client.construct_query_vars(lat_lng=(12.3456, -10.432))
        self.assertEqual(qv, {
                'lat': 12.3456,
                'lng': -10.432, 
                'api_key': self.api_key,
            })
        