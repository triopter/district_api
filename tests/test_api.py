from unittest import TestCase

from district_api.api import DistrictApi, District, DistrictApiError, \
    ApiUnavailable, LocationUnavailable, AuthorizationError, QuotaExceeded

class ApiTestCase(TestCase):
    def setUp(self):
        self.client = DistrictApi('dummy')
        
    def test_construction(self):
        self.assertEqual(self.client.api_key, 'dummy')
        self.assertEqual(self.client.url, 'http://api.nytimes.com/svc/politics/v2/districts.json')

        other_client = DistrictApi('dummy', url='http://www.example.com')
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