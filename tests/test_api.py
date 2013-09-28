from unittest import TestCase
import requests
from mock import patch, Mock

from district_api.api import DistrictApi, District, DistrictApiError, \
    ApiUnavailable, LocationUnavailable, AuthorizationError, QuotaExceeded, \
    BadRequest

class ApiTestCase(TestCase):
    api_key = 'dummy'
    url = 'http://api.nytimes.com/svc/politics/v2/districts.json'

    def setUp(self):
        self.client = DistrictApi(self.api_key)
        
    def test_construction(self):
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client.url, self.url)

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
            self.fail('get_districts should accept float, int, and strings that '
                'can be converted to floats/ints')
                
    def test_construct_query_vars(self):
        qv = self.client.construct_query_vars(lat_lng=(12.3456, -10.432))
        self.assertEqual(qv, {
                'lat': 12.3456,
                'lng': -10.432, 
                'api_key': self.api_key,
            })
    
    @patch('requests.get')
    def test_send_request(self, get):
        self.client.send_request(lat_lng=(12.3456, -10.432))
        self.assertTrue(get.called)
        get.assert_called_with(self.url, params={
                'lat': 12.3456,
                'lng': -10.432, 
                'api_key': self.api_key,
            })
            
        self.client.send_request()
        self.assertTrue(get.called)
        get.assert_called_with(self.url, params={
                'api_key': self.api_key,
            })
            
    def test_validate_status(self):
        with self.assertRaises(ApiUnavailable):
            mock = Mock(None)
            mock.status_code = 404
            self.client.validate_response(mock)
            
        with self.assertRaises(ApiUnavailable):
            mock = Mock(None)
            mock.status_code = 500
            self.client.validate_response(mock)
            
        with self.assertRaises(BadRequest):
            mock = Mock(None)
            mock.status_code = 400
            self.client.validate_response(mock)
            
        with self.assertRaises(AuthorizationError):
            mock = Mock(None)
            mock.status_code = 403
            self.client.validate_response(mock)
            
        with self.assertRaises(DistrictApiError):
            mock = Mock(None)
            mock.status_code = 406
            self.client.validate_response(mock)
            
        # Make sure it doesn't raise on 200:
        try:
            mock = Mock(None)
            mock.status_code = 200
            self.client.validate_response(mock)
        except:
            self.fail('validate_response should not raise any errors for a 200 '
                'status code')
            
            
            
            
            